# AI Security Lab

Local AI Security Lab for experimenting with agentic AI security controls, RAG security, guardrails, policy-as-code, and SIEM observability.

This project is a hands-on lab environment for learning how to design, build, test, monitor, and break defensive controls around local AI systems. The initial goal is not to build a production-ready AI platform, but to create a controlled local environment where AI security concepts can be tested practically.

## Purpose

The purpose of this project is to explore security controls for modern AI systems, especially systems that use:

- Local large language models
- Retrieval-augmented generation
- Agentic workflows
- Tool calling
- Policy-as-code
- Guardrails
- Structured logging
- SIEM-based detection

The project is based on the idea that AI systems should be treated as security-relevant software systems with their own attack surface, telemetry, controls, and failure modes.

## Core Security Themes

This lab focuses on the following security topics:

- Prompt injection
- Indirect prompt injection through retrieved documents
- RAG poisoning
- Tool misuse
- Excessive agency
- Agent identity and authorization
- Session and context isolation
- Unsafe output handling
- Multi-agent delegation risks
- Human-in-the-loop approval
- Kill switch mechanisms
- AI-specific logging and detection engineering

## Target Architecture

The intended architecture is a local agentic AI security environment.

```text
User
  |
  v
Web UI / Chat UI
  |
  v
AI Gateway
  |-- input validation
  |-- policy checks
  |-- prompt injection detection
  |-- rate limiting
  |-- structured logging
  |
  v
Agent Runtime
  |-- Research Agent
  |-- later: Guard Agent / Review Agent
  |
  +-- RAG Tool
  |     |-- PDF document store
  |     |-- Vector database
  |     |-- metadata and ACL checks
  |
  +-- Approved Tools
  |     |-- search_documents
  |     |-- read_document_chunk
  |     |-- create_answer_with_citations
  |
  v
Local LLM
  |-- Gemma via Ollama
  |
  v
Observability
  |-- JSON logs
  |-- OpenTelemetry Collector
  |-- Wazuh SIEM
