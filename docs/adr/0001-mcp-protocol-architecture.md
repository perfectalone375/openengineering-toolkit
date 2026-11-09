# ADR 0001: Model Context Protocol (MCP) Standard for Tool Augmentation

## Status
Accepted

## Context
AI coding assistants and autonomous agents (Claude 3.5 Sonnet, Cursor, Gemini, Antigravity) frequently hallucinate or produce rounding errors when tasked with calculating multi-term engineering equations (e.g., Tsiolkovsky rocket delta-v, Rankine-Hugoniot normal shock discontinuities, and Euler-Bernoulli beam deflections).

To ground language models in deterministic engineering mechanics, we evaluated:
1. **Custom Python Function Calling (OpenAI / Anthropic specific schemas):** Fragmented across vendors and requires proprietary middleware.
2. **REST Webhooks (FastAPI endpoints):** High latency for local IDE workflows; requires external port management and networking tunnels.
3. **Model Context Protocol (MCP stdio/JSON-RPC 2.0):** Open industry standard supported natively by Claude Desktop, Cursor, and modern developer environments. Uses standard input/output streams with low latency (<5 ms) and strict schema validation.

## Decision
We adopted the **Model Context Protocol (MCP)** specification (Protocol version `2024-11-05`) as the primary integration interface for computational tools.

## Architecture
- All core analytical functions in `openengineering` are wrapped in MCP tool declarations.
- Communication uses line-delimited JSON-RPC 2.0 over standard I/O (`sys.stdin` / `sys.stdout`).
- Strict JSON Schema parameter definitions ensure LLMs pass validated numerical inputs with units.

## Consequences
- **Positive:** Enables instant, zero-configuration local tool calling in Claude Desktop and Cursor.
- **Positive:** Eliminates mathematical hallucinations for compressible flow and propulsion thermodynamics.
- **Neutral:** Stdio transports require unbuffered execution (`python -u` or explicit `flush=True`).

