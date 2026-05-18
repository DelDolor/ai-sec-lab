# Implementation Plan

## Phase 0 — Repository Skeleton (current)

Goal: safe, documented starting point with no real implementation yet.

- [x] Directory structure
- [x] Placeholder FastAPI services (health endpoints only)
- [x] Docker Compose with all services declared
- [x] Policy YAML files (tool policy, guardrails, prompts, access control)
- [x] OpenTelemetry Collector config
- [x] Wazuh decoder and detection rules
- [x] Synthetic example security events
- [x] Architecture and threat model documentation
- [x] Security notes for public repo contributors

---

## Phase 1 — Working RAG Pipeline

Goal: ingest PDFs, store embeddings in Qdrant, return real search results.

- [ ] `rag-ingestion`: implement PDF → text extraction (PyMuPDF or pdfminer)
- [ ] `rag-ingestion`: implement text chunking with configurable overlap
- [ ] `rag-ingestion`: implement embedding generation (local model via Ollama or sentence-transformers)
- [ ] `rag-ingestion`: implement Qdrant upload with document metadata
- [ ] `agent-runtime`: implement `search_documents` tool (Qdrant query)
- [ ] `agent-runtime`: implement `read_document_chunk` tool (fetch by ID)
- [ ] Health endpoints: return real Qdrant and Ollama connectivity status
- [ ] Integration test: ingest a sample document, search for a known term

---

## Phase 2 — Guardrails and Policy Enforcement

Goal: policy files are loaded and enforced at runtime.

- [ ] `ai-gateway`: load and apply `input-policy.yaml` at request time
- [ ] `ai-gateway`: implement prompt injection pattern matching
- [ ] `ai-gateway`: implement rate limiting (in-memory for local lab)
- [ ] `ai-gateway`: emit structured `ai.policy.decision` log events via OTEL
- [ ] `agent-runtime`: enforce tool allowlist from `tool-policy.yaml`
- [ ] `agent-runtime`: enforce `max_tool_calls_per_request` and `max_retrieved_chunks`
- [ ] `agent-runtime`: emit `ai.tool_call.denied` events for blocked tool calls
- [ ] `ai-gateway`: apply `output-policy.yaml` before returning responses
- [ ] Unit tests for each policy check

---

## Phase 3 — Agent Security Controls

Goal: full ResearchAgent with security controls, observable kill switch.

- [ ] `agent-runtime`: implement ResearchAgent loop (query → retrieve → synthesize)
- [ ] `agent-runtime`: implement `create_answer_with_citations` tool
- [ ] `agent-runtime`: enforce system prompt from `research-agent.yaml`
- [ ] `agent-runtime`: implement session isolation (per-request context only)
- [ ] `agent-runtime`: implement kill switch (stops agent at next tool boundary)
- [ ] `agent-runtime`: emit `ai.kill_switch.activated` event when triggered
- [ ] Lab experiment: indirect prompt injection via poisoned document
- [ ] Lab experiment: RAG poisoning detection scenario
- [ ] Lab experiment: tool misuse attempt (verify denial and logging)

---

## Phase 4 — Full Observability and SIEM Integration

Goal: all security events reach Wazuh; detection rules fire correctly.

- [ ] Validate OTEL Collector pipeline: traces and logs flowing correctly
- [ ] Connect OTEL Collector output to Wazuh agent or syslog forwarder
- [ ] Test Wazuh decoders against live `ai-security-events.jsonl` format
- [ ] Validate each Wazuh rule fires against a corresponding synthetic event
- [ ] Add frequency-based alerting test (5 tool denials in 60 seconds)
- [ ] Document Wazuh setup steps (external — not deployed in this repo)
- [ ] Add Grafana/Prometheus metrics for gateway throughput and policy decisions (optional)
