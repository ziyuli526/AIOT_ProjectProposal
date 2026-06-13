from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from schemas import AskRequest, AskResponse, ErrorResponse, HistoryResponse
from services.firebase_data_service import FirebaseDataService
from services.llm_service import LLMService

# Initialize FastAPI application
app = FastAPI(
    title="AI Hydration Assistant Backend",
    description="Backend service connecting Firebase RTDB IoT metrics to OpenAI for smart hydration suggestions.",
    version="1.0.0"
)

# Enable CORS for frontend applications running locally
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize singletons for services
firebase_service = FirebaseDataService()
llm_service = LLMService()

@app.get("/")
async def health_check():
    """
    Simple health check endpoint.
    """
    return {"message": "AI Hydration Assistant API is running"}

@app.post(
    "/ask",
    response_model=AskResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Validation or configuration error"},
        500: {"model": ErrorResponse, "description": "Firebase or OpenAI service error"}
    }
)
async def ask_question(request: AskRequest):
    """
    Handles question submission from the frontend.
    1. Validates that the question is non-empty.
    2. Reads the latest hydration and IoT metrics from Firebase.
    3. Transforms metrics to a context dictionary.
    4. Submits the prompt to OpenAI and returns the answer.
    """
    # 1. Receive and validate question
    question = request.question
    if not question or not question.strip():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Question must not be empty or whitespace."}
        )

    # 2. Read latest data from Firebase path `/health/today`
    try:
        hydration_data = firebase_service.fetch_today_hydration_data()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Firebase read failed: {str(e)}"}
        )

    # 3. Build hydration context dictionary
    context = hydration_data.to_context_dict()

    # 4. Build system/user prompt and call LLM API
    try:
        answer = llm_service.ask_hydration_assistant(question, context)
        return AskResponse(answer=answer)
    except ValueError as ve:
        # Missing configuration or invalid model input
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": f"Configuration error: {str(ve)}"}
        )
    except Exception as e:
        # LLM execution error
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"LLM service error: {str(e)}"}
        )

@app.get(
    "/api/history",
    response_model=HistoryResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Firebase service error"}
    }
)
async def get_history():
    """
    Fetches the latest hydration metrics from Firebase and returns them.
    """
    try:
        hydration_data = firebase_service.fetch_today_hydration_data()
        return HistoryResponse(
            current_ml=hydration_data.drank_water,
            target_ml=hydration_data.target_water,
            percentage=round(hydration_data.achievement_percentage, 2),
            remaining_ml=hydration_data.calculated_remaining_water
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Firebase read failed: {str(e)}"}
        )
