# AI Security Lab

Local AI Security Lab for experimenting with agentic AI security controls, RAG security, guardrails, policy-as-code, and SIEM observability.

> **Public repository.** This repo contains no secrets, credentials, private data, real logs, real PDFs, or home lab details. See [docs/security-notes.md](docs/security-notes.md) before contributing.

---

## What This Is

A hands-on local lab environment for learning how to design, build, test, monitor, and break defensive controls around local AI systems. The goal is a controlled learning environment — not a production platform.

## What Is Intentionally Not Included

- Real API keys, tokens, or credentials
- Real PDF documents or training material
- Real log data or session data
- IP addresses, hostnames, or internal network details
- Personal information of any kind

All environment variables go in `.env.example` with placeholder values only. Real values live in `.env`, which is gitignored.

## Security Topics Covered

- Prompt injection and indirect prompt injection via RAG
- RAG poisoning
- Tool misuse and excessive agency
- Agent identity and authorization
- Session and context isolation
- Unsafe output handling
- Multi-agent delegation risks
- Human-in-the-loop approval and kill switches
- AI-specific structured logging and SIEM detection engineering

## Target Architecture

```text
User
  │
  ▼
Web UI / Chat UI
  │
  ▼
AI Gateway                    ← input validation, policy checks, prompt injection
  │                              detection, rate limiting, structured logging
  ▼
Agent Runtime                 ← ResearchAgent with approved tool use only
  ├── RAG Tool                ← Qdrant vector DB + metadata/ACL checks
  └── Approved Tools          ← search_documents, read_document_chunk,
                                 create_answer_with_citations
  │
  ▼
Local LLM (Gemma via Ollama)
  │
  ▼
Observability                 ← JSON logs → OpenTelemetry → Wazuh SIEM
```

Wazuh is an external SIEM target. It is not deployed inside this repository.

## Repository Layout

```
apps/
  ai-gateway/       FastAPI: input validation, policy enforcement, gateway
  agent-runtime/    FastAPI: ResearchAgent with approved tools
  rag-ingestion/    FastAPI/CLI: PDF ingestion into Qdrant
policies/
  prompts/          Agent system prompt policies
  tools/            Tool allow/deny list and limits
  guardrails/       Input and output guardrail policies
  access/           Document-level ACL policies
observability/
  otel-collector/   OpenTelemetry Collector config
  wazuh/            Wazuh decoders and detection rules
  examples/         Synthetic example security events
data/
  documents/        Local PDFs for RAG (gitignored)
  poisoned-docs/    Adversarial test documents (gitignored)
  uploads/          Staging area (gitignored)
docs/               Architecture, threat model, implementation plan
```

## MVP Scope

Phase 0 (current): Repository skeleton — directory structure, placeholder services, policy files, observability config, Wazuh detection rules, documentation.

Phase 1: Working RAG pipeline — PDF ingestion into Qdrant, basic document search, health endpoints returning real status.

Phase 2: Guardrails and policy enforcement — input validation, prompt injection detection, output filtering, policy-as-code integration.

Phase 3: Agent security controls — ResearchAgent with approved tools only, tool call logging, session isolation, kill switch mechanism.

Phase 4: Full observability — structured JSON logs, OpenTelemetry traces, Wazuh SIEM integration with live detection rules.

## Local Development (Placeholder Phase)

**Requirements:** Docker, Docker Compose, Python 3.11+

```bash
# Copy environment template — fill in values as needed
cp .env.example .env

# Start all services
docker compose up --build

# Health checks
curl http://localhost:8000/health   # ai-gateway
curl http://localhost:8001/health   # agent-runtime
curl http://localhost:8002/health   # rag-ingestion

# Run tests for a single app
cd apps/ai-gateway
pip install -e ".[dev]"
pytest

# Run tests for all apps
for app in apps/*/; do
  echo "=== $app ===" && (cd "$app" && pip install -e ".[dev]" && pytest)
done
```

## Non-Goals

- Production deployment
- Cloud services of any kind
- Multi-user or multi-tenant access control
- Kubernetes
- Full-featured chat UI
- Model fine-tuning
