import logging
from openai import OpenAI
import config
from prompts.prompt_builder import PromptBuilder

logger = logging.getLogger("hydration_backend")

class LLMService:
    def __init__(self):
        self.api_key = config.OPENAI_API_KEY
        self.model = config.LLM_MODEL
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)

    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """
        Calls the OpenAI API using the system and user prompts.
        Checks for API key presence and handles exceptions gracefully.
        """
        if not self.api_key:
            raise ValueError("OpenAI API key is missing. Please configure OPENAI_API_KEY in your env.")

        if not self.client:
            self.client = OpenAI(api_key=self.api_key)

        try:
            # 1. Attempt the user's expected "client.responses.create" format if possible
            if hasattr(self.client, 'responses'):
                logger.info(f"Attempting to use OpenAI Responses API with model: {self.model}")
                try:
                    response = self.client.responses.create(
                        model=self.model,
                        input=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=0.7
                    )
                    # Check if response has output_text attribute as expected
                    if hasattr(response, 'output_text') and response.output_text:
                        return response.output_text
                    elif hasattr(response, 'choices') and len(response.choices) > 0:
                        choice = response.choices[0]
                        if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                            return choice.message.content
                except Exception as ex:
                    logger.warning(f"Responses API call failed, falling back to Chat Completions: {ex}")

            # 2. Fallback to standard chat completions API
            logger.info(f"Using fallback Chat Completions API with model: {self.model}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise RuntimeError(f"OpenAI API call failed: {e}")

    def ask_hydration_assistant(self, question: str, context: dict) -> str:
        """
        Coordinates constructing prompts and calling the LLM to get the final response.
        """
        system_prompt = PromptBuilder.build_system_prompt()
        user_prompt = PromptBuilder.build_user_prompt(question, context)
        return self.generate_response(system_prompt, user_prompt)
