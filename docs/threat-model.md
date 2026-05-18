# Threat Model

This document captures the threat model for the AI Security Lab. The lab is a local learning environment, not a production system. The threats below reflect both real AI security risks (which the lab is designed to study) and operational risks (leaking lab data into the public repository).

---

## Threat Actors

| Actor | Goal | Relevance |
|---|---|---|
| Adversarial user | Manipulate the AI agent via crafted inputs | Primary attack surface for lab experiments |
| Malicious document author | Poison the RAG corpus to redirect agent behavior | Indirect prompt injection experiments |
| Lab operator (accidental) | Commit secrets or private data to the public repo | Operational risk — see `docs/security-notes.md` |

---

## Attack Vectors by Component

### AI Gateway

| Threat | Description | Control |
|---|---|---|
| Prompt injection | User input contains instructions targeting the LLM | `input-policy.yaml` pattern matching, gateway blocks |
| Rate abuse | Flooding the gateway to degrade availability or brute-force inputs | Rate limiting per session |
| Oversized input | Sending payloads too large for safe processing | Max input length check |
| Session confusion | Crafted session IDs to access another session's context | Session boundary enforcement |

### Agent Runtime

| Threat | Description | Control |
|---|---|---|
| Tool misuse | Agent attempts to call a non-approved tool | Tool allowlist in `tool-policy.yaml`; denied calls logged |
| Excessive agency | Agent takes unrequested autonomous actions | Read-only tool set; no write/exec/network tools |
| Kill switch bypass | Agent continues execution after stop signal | Kill switch checked at each tool call boundary |
| Multi-agent delegation | Agent delegates to an unauthorized sub-agent | Not implemented; no sub-agent capability in MVP |

### RAG Pipeline

| Threat | Description | Control |
|---|---|---|
| Indirect prompt injection | Retrieved document contains instructions to the agent | System prompt explicitly treats retrieved content as untrusted |
| RAG poisoning | Adversary inserts documents designed to alter agent behavior | `data/poisoned-docs/` used for controlled experiments; ACL on collections |
| Over-retrieval | Agent retrieves too many chunks, increasing attack surface | `max_retrieved_chunks: 8` in tool policy |
| ACL bypass | Agent retrieves documents it should not have access to | Document ACL enforced in `document-access.yaml` |

### LLM (Ollama / Gemma)

| Threat | Description | Control |
|---|---|---|
| System prompt override | Injected content overrides system instructions | System prompt constraint: document content cannot override instructions |
| Hallucination | Agent invents citations or facts not in the document store | Output guardrail requires citations; `hallucination_guard` flag |
| Unsafe output | Agent produces harmful, private, or sensitive content | Output guardrail pattern checks |

### Observability

| Threat | Description | Control |
|---|---|---|
| Log injection | Crafted input that corrupts structured log fields | Structured JSON logging with typed fields; untrusted content is a string value, not a key |
| Missing events | Security-relevant events not reaching SIEM | All gateway decisions and tool calls logged; OTEL pipeline |

---

## MITRE ATLAS Mapping (Partial)

| Technique | Lab Scenario |
|---|---|
| AML.T0051 - LLM Prompt Injection | Prompt injection experiments via the gateway |
| AML.T0054 - LLM Jailbreak | Testing guardrail bypass resistance |
| AML.T0019 - Publish Poisoned Data | RAG poisoning via `data/poisoned-docs/` |
| AML.T0048 - Exfiltration via ML Model | Testing if the agent can be made to leak context |

---

## Out of Scope (for this lab)

- Network-level attacks (the lab has no exposed public endpoints)
- Supply chain attacks on model weights
- Physical access threats
- Cloud or multi-tenant scenarios
