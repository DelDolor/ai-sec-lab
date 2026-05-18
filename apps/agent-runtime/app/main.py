from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Agent Runtime",
    description="ResearchAgent execution with approved-tools-only enforcement.",
)


class AgentRequest(BaseModel):
    query: str
    session_id: str = "example-session-id"
    user_id: str = "local-user"


class AgentResponse(BaseModel):
    answer: str
    sources: list[str]
    tool_calls_made: list[str]


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "agent-runtime"}


@app.post("/agent/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest) -> AgentResponse:
    # Placeholder: real implementation will run the ResearchAgent loop:
    # query → search_documents → read_document_chunk → create_answer_with_citations.
    # Tool calls are enforced against tool-policy.yaml; all calls are logged via OTEL.
    return AgentResponse(
        answer="[placeholder] Agent received query. ResearchAgent not yet implemented.",
        sources=[],
        tool_calls_made=[],
    )
