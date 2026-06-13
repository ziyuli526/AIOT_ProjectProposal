from pydantic import BaseModel, Field, field_validator

class AskRequest(BaseModel):
    question: str = Field(..., description="The hydration-related question asked by the user.")

    @field_validator("question")
    @classmethod
    def validate_question_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Question cannot be empty or only whitespace.")
        return v.strip()

class AskResponse(BaseModel):
    answer: str = Field(..., description="The AI assistant's response to the user's question.")

class HistoryResponse(BaseModel):
    current_ml: float = Field(..., description="Current water drank in mL.")
    target_ml: float = Field(..., description="Target water to drink in mL.")
    percentage: float = Field(..., description="Percentage of target reached.")
    remaining_ml: float = Field(..., description="Remaining water to drink in mL.")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message describing what went wrong.")
