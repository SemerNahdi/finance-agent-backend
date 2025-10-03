from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.core import process_query

router = APIRouter()


class AgentRequest(BaseModel):
    user_id: str
    query: str


class AgentResponse(BaseModel):
    text: str
    chart_path: str = None
    csv_path: str = None


@router.post("/", response_model=AgentResponse)
async def agent_endpoint(request: AgentRequest):
    # Call core agent logic
    response = await process_query(request.user_id, request.query)
    return response
