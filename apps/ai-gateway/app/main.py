from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="AI Gateway",
    description="Input validation and policy enforcement layer for the AI Security Lab.",
)


class ChatRequest(BaseModel):
    message: str
    session_id: str = "example-session-id"
    user_id: str = "local-user"


class ChatResponse(BaseModel):
    response: str
    session_id: str
    policy_decision: str


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "ai-gateway"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    # Placeholder: real implementation will apply input-policy.yaml checks
    # (injection detection, rate limiting, length validation), log a policy decision
    # event via OTEL, then forward the request to agent-runtime.
    return ChatResponse(
        response="[placeholder] Gateway received message. Policy enforcement not yet implemented.",
        session_id=request.session_id,
        policy_decision="allowed",
    )
