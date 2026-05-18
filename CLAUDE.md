# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A local AI Security Lab for experimenting with agentic AI security controls, RAG security, guardrails, policy-as-code, and Wazuh SIEM observability. This is a **public repository** — no secrets, real PDFs, real logs, or private network details belong here. See `docs/security-notes.md` before committing anything.

## What We Are Building

A locally-hosted, multi-service AI pipeline where every component boundary is a security control point. The goal is not a production system but a hands-on lab for studying and breaking AI security controls:

- **Prompt injection and indirect prompt injection** via crafted user input and poisoned RAG documents
- **RAG poisoning** — adversarial documents in `data/poisoned-docs/` that try to redirect agent behavior
- **Tool misuse and excessive agency** — testing whether the agent stays within its approved tool set
- **Guardrails and policy-as-code** — YAML-driven input/output validation enforced at the gateway
- **Structured AI security logging** — every policy decision and tool call emits a typed JSON event
- **Wazuh SIEM detection engineering** — custom decoders and rules that fire on AI-specific event types

## Current State (Phase 0 — skeleton, committed 2026-05-18)

The full repository skeleton is built and pushed to `github.com/DelDolor/ai-sec-lab`. Everything below exists but none of the core logic is implemented yet — all three apps return placeholder responses.

### What exists

| Area | Files | Status |
|---|---|---|
| AI Gateway | `apps/ai-gateway/app/main.py` | `GET /health`, `POST /chat` — placeholder only |
| Agent Runtime | `apps/agent-runtime/app/main.py` | `GET /health`, `POST /agent/run` — placeholder only |
| RAG Ingestion | `apps/rag-ingestion/app/main.py` | `GET /health` — placeholder only |
| Docker Compose | `docker-compose.yml` | All 6 services declared (gateway, agent, rag, qdrant, ollama, otel-collector) |
| Policy files | `policies/` | Tool allowlist, input/output guardrails, agent system prompt, document ACL — YAML only, not loaded at runtime yet |
| Observability | `observability/otel-collector/config.yaml` | Config ready, not wired to services yet |
| Wazuh | `observability/wazuh/decoders/` + `rules/` | Decoders and rules for 5 event types, rule IDs 100100–100112 |
| Example events | `observability/examples/ai-security-events.jsonl` | 11 synthetic events covering all event types |
| Tests | `apps/*/tests/test_health.py` | 5 tests, all passing |
| Docs | `docs/` | Architecture, threat model, 4-phase implementation plan, security notes |

### What does NOT exist yet

- Policy files are not loaded or enforced at runtime
- No real RAG pipeline (no PDF parsing, no embeddings, no Qdrant queries)
- No agent logic (ResearchAgent loop is not implemented)
- No OTEL instrumentation in the apps
- No Wazuh connection

## Next Steps (Phase 1)

The implementation plan is in `docs/implementation-plan.md`. The logical next session is **Phase 1 — Working RAG Pipeline**:

1. `rag-ingestion`: PDF → text extraction → chunking → embedding → Qdrant upload
2. `agent-runtime`: implement `search_documents` and `read_document_chunk` tools
3. Health endpoints: return real Qdrant and Ollama connectivity status
4. Integration test: ingest a sample document and verify a search hit

## Commands

Each app is a self-contained Python package. Run from the app directory:

```bash
# Install with dev dependencies
python3 -m pip install -e ".[dev]"

# Run tests
python3 -m pytest -v

# Lint
ruff check .

# Type check
mypy .
```

Run all app tests from repo root:
```bash
for app in apps/*/; do
  echo "=== $app ===" && (cd "$app" && python3 -m pip install -e ".[dev]" && python3 -m pytest -v)
done
```

Start all services:
```bash
cp .env.example .env   # fill in real values
docker compose up --build
```

Health checks: `localhost:8000/health` (gateway), `localhost:8001/health` (agent), `localhost:8002/health` (rag-ingestion).

**Note:** `pip` is not on PATH in this environment — use `python3 -m pip` and `python3 -m pytest` instead.

## Architecture

```
User → AI Gateway (:8000) → Agent Runtime (:8001) → Qdrant (:6333) + Ollama (:11434)
                                                   ↓
                              OTEL Collector (:4317) → [Wazuh SIEM — external]
```

- **AI Gateway** (`apps/ai-gateway/`) — FastAPI. Will validate input, apply `policies/guardrails/input-policy.yaml`, log all policy decisions via OTEL, forward to agent-runtime.
- **Agent Runtime** (`apps/agent-runtime/`) — FastAPI. Will run ResearchAgent with a strict tool allowlist from `policies/tools/tool-policy.yaml`. System prompt from `policies/prompts/research-agent.yaml`.
- **RAG Ingestion** (`apps/rag-ingestion/`) — FastAPI. Will ingest PDFs from `data/documents/` into Qdrant.
- **Policy files** (`policies/`) — YAML configs to be loaded at runtime. Guardrails, tool policy, prompt, and document ACL.
- **Observability** (`observability/`) — OTEL Collector config + Wazuh decoder/rules. Security events: `ai.prompt_injection.detected`, `ai.tool_call.denied`, `ai.rag.poisoning_suspected`, `ai.kill_switch.activated`, `ai.policy.decision`.

## Key Security Invariants

- Retrieved RAG documents are **untrusted context** — document content must never override the system prompt or tool policy (see `policies/prompts/research-agent.yaml`).
- Tool calls are restricted to the allowlist in `policies/tools/tool-policy.yaml`; any denied call emits `ai.tool_call.denied`.
- All policy decisions are logged as structured JSON for SIEM ingestion.
- `data/documents/`, `data/poisoned-docs/`, and `data/uploads/` are gitignored — never add real PDFs.
- `.claude/settings.local.json` is gitignored — local Claude Code permissions stay local.

## Wazuh Rule IDs

Custom rules use IDs `100100–100199`. Frequency-based rules: 100110 (5 tool denials in 60s), 100111 (3 injection attempts in 120s), 100112 (2 RAG poisoning detections in 300s).
