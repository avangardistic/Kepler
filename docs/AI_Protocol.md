# AI Protocol

## Structure
- LLM generates HFT research
- Mathematical formalism only, no code unless validated
- Documentation-first, code-second

## Rules
- Do not execute trading strategies
- Do not use external parameters without documenting the violation
- Every claim must have a rejection criterion
- Maintain synchronization with other agents via Paperclip

## Coordination
- Use Paperclip for inter-agent communication
- Fallback: AgentSync.md for state handoff
- All state changes logged in ResearchLog.md
