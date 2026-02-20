from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

from .optimizer import generate_team

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SynergySelect AI", description="Intelligent Team-as-a-Service Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TeamFormationRequest(BaseModel):
    department: str
    team_size: int
    total_budget: float

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/v1/team/generate")
def create_team(request: TeamFormationRequest):
    logger.info(f"Received request for department {request.department}, team_size {request.team_size}, budget {request.total_budget}")
    try:
        result = generate_team(
            department=request.department,
            team_size=request.team_size,
            total_budget=request.total_budget
        )
        return result
    except Exception as e:
        logger.error(f"Error generating team: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
