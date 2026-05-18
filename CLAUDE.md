# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A local AI Security Lab for experimenting with agentic AI security controls, RAG security, guardrails, policy-as-code, and Wazuh SIEM observability. This is a **public repository** — no secrets, real PDFs, real logs, or private network details belong here. See `docs/security-notes.md` before committing anything.

## Commands

Each app is a self-contained Python package. Run from the app directory:

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check .

# Type check
mypy .
```

Run all app tests from repo root:
```bash
for app in apps/*/; do
  echo "=== $app ===" && (cd "$app" && pip install -e ".[dev]" && pytest)
done
```

Start all services:
```bash
cp .env.example .env   # fill in real values
docker compose up --build
```

Health checks: `localhost:8000/health` (gateway), `localhost:8001/health` (agent), `localhost:8002/health` (rag-ingestion).

## Architecture

```
User → AI Gateway (:8000) → Agent Runtime (:8001) → Qdrant (:6333) + Ollama (:11434)
                                                   ↓
                              OTEL Collector (:4317) → [Wazuh SIEM — external]
```

- **AI Gateway** (`apps/ai-gateway/`) — FastAPI. Validates input, applies `policies/guardrails/input-policy.yaml`, logs all policy decisions via OTEL, forwards to agent-runtime.
- **Agent Runtime** (`apps/agent-runtime/`) — FastAPI. Runs ResearchAgent with a strict tool allowlist from `policies/tools/tool-policy.yaml`. System prompt loaded from `policies/prompts/research-agent.yaml`.
- **RAG Ingestion** (`apps/rag-ingestion/`) — FastAPI. Ingests PDFs from `data/documents/` into Qdrant. Not yet implemented beyond health endpoint.
- **Policy files** (`policies/`) — YAML configs loaded at runtime; not baked into service images. Guardrails, tool policy, prompt, and document ACL live here.
- **Observability** (`observability/`) — OTEL Collector config + Wazuh decoder/rules. All security events (injection detected, tool denied, kill switch, policy decision) emit structured JSON via OTEL.

## Key Security Invariants

- Retrieved RAG documents are **untrusted context** — document content must never override the system prompt or tool policy (enforced in `research-agent.yaml`).
- Tool calls are restricted to the allowlist in `tool-policy.yaml`; any denied call emits an `ai.tool_call.denied` event.
- All policy decisions are logged as structured JSON for SIEM ingestion.
- `data/documents/`, `data/poisoned-docs/`, and `data/uploads/` are gitignored — never add real PDFs.

## Wazuh Rule IDs

Custom rules use IDs `100100–100199`. See `observability/wazuh/rules/ai-security-rules.xml` and the synthetic event examples in `observability/examples/ai-security-events.jsonl`.

## Current Phase

Phase 0 (skeleton). All three apps return placeholder responses. See `docs/implementation-plan.md` for what comes next.
