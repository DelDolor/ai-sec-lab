# Architecture

## Overview

The lab is a locally-hosted, multi-service AI pipeline with a security-first design. Every component boundary is a control point: the gateway validates input before it reaches the agent, the agent is restricted to approved tools only, and every significant event is logged in a structured format suitable for SIEM ingestion.

## Component Map

```
┌─────────────────────────────────────────────────────────────────┐
│ LOCAL HOST                                                      │
│                                                                 │
│  ┌──────────────┐    ┌─────────────────────────────────────┐   │
│  │   User /     │    │           AI Gateway :8000           │   │
│  │  Chat UI     │───▶│  • Input validation                  │   │
│  └──────────────┘    │  • Prompt injection detection        │   │
│                      │  • Policy checks (input-policy.yaml) │   │
│                      │  • Rate limiting                     │   │
│                      │  • Structured logging (OTEL)         │   │
│                      └──────────────┬──────────────────────┘   │
│                                     │                           │
│                      ┌──────────────▼──────────────────────┐   │
│                      │       Agent Runtime :8001            │   │
│                      │  • ResearchAgent (read-only)         │   │
│                      │  • Tool call enforcement             │   │
│                      │  • Session isolation                 │   │
│                      │  • Kill switch mechanism             │   │
│                      └──┬───────────────────────┬──────────┘   │
│                         │                       │               │
│           ┌─────────────▼──────┐    ┌───────────▼────────────┐ │
│           │    RAG Tool        │    │    Approved Tools       │ │
│           │  • Qdrant :6333    │    │  search_documents       │ │
│           │  • ACL checks      │    │  read_document_chunk    │ │
│           │  • Metadata filter │    │  create_answer_...      │ │
│           └────────────────────┘    └────────────────────────┘ │
│                                                                 │
│  ┌──────────────────────┐   ┌───────────────────────────────┐  │
│  │  RAG Ingestion :8002 │   │     Ollama :11434             │  │
│  │  • PDF → chunks      │   │     • Gemma 7B (local)        │  │
│  │  • Embeddings        │   │     • No external calls       │  │
│  │  • Qdrant upload     │   └───────────────────────────────┘  │
│  └──────────────────────┘                                       │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Observability                                           │   │
│  │  OTEL Collector :4317/4318  →  [Wazuh SIEM external]    │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow: Normal Request

1. User sends a message to the AI Gateway (`POST /chat`).
2. Gateway validates input against `input-policy.yaml` (length, injection patterns, rate limit).
3. Gateway logs the policy decision as a structured JSON event → OTEL Collector.
4. If allowed, gateway forwards the request to Agent Runtime (`POST /agent/run`).
5. Agent Runtime queries Qdrant via the RAG Tool (up to `max_retrieved_chunks: 8`).
6. Each retrieved chunk is treated as untrusted context (see `research-agent.yaml`).
7. Agent calls the local LLM via Ollama to compose an answer with citations.
8. Output passes through `output-policy.yaml` checks before being returned.
9. Every tool call is logged; denied tool calls emit `ai.tool_call.denied` events.

## Security Boundaries

| Boundary | Control |
|---|---|
| User → Gateway | Input guardrails, injection detection, rate limit |
| Gateway → Agent | Authenticated internal call; session ID propagated |
| Agent → Tools | Strict allowlist; all calls logged |
| Agent → LLM | Local Ollama only; no external LLM calls |
| Retrieved docs → Agent | Documents treated as untrusted; system prompt cannot be overridden |
| Any service → outside | No egress; all services are Docker-internal |

## Policy Files

| File | Purpose |
|---|---|
| `policies/tools/tool-policy.yaml` | Tool allowlist, deny list, and call limits |
| `policies/prompts/research-agent.yaml` | System prompt with RAG security constraints |
| `policies/guardrails/input-policy.yaml` | Input validation rules |
| `policies/guardrails/output-policy.yaml` | Output filtering rules |
| `policies/access/document-access.yaml` | Document-level ACL by role |

## Storage

| Service | Volume | Gitignored |
|---|---|---|
| Qdrant | `./storage/qdrant` | Yes |
| Ollama models | `./storage/ollama` | Yes |
| Ingestable PDFs | `./data/documents` | Yes |
| Adversarial docs | `./data/poisoned-docs` | Yes |
