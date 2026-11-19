# Prompt trace

## Interaction 1

**Prompt:** Explain the content of `NOTES.md`. Execute `AGENTS.md`.

**Response:** `NOTES.md` describes an AI study/project in wealth and asset management. Its goal is to build an AI overlay for self-directed investor accounts, generally with under $500,000 invested, that can manage investments discretionarily when the client consents. It identifies Python and React plus AI/LLM and agent skills; Cursor as the tool; and focus areas including agentic architecture, RAG, harnesses, validation, code reviews, observability, evaluation, human oversight, LangChain/LangGraph, Langfuse/LangSmith, and guardrails. The domain topics are self-directed versus discretionary accounts, robo-advisors, portfolio rebalancing, and risk profiling.

## Interaction 2

**Prompt:** We have to build an agent using the info in `NOTES.md` for learning purpose.

**Response:** Created a dependency-free Python CLI learning prototype with a local wealth-management knowledge base, keyword retrieval, a deterministic mock-model drafting step, request classification, a visible workflow trace, human-review routing for personal decisions, and transaction execution disabled. Added a README with the learning path and five focused tests; all tests pass, and the CLI was exercised with educational and personal-decision queries.

## Interaction 3

**Prompt:** Implement the Chat Customizations Evaluations suggestion in `AGENTS.md`: replace the ambiguous phrase “any info” with “all relevant information, including responses and intermediate reasoning”.

**Response:** Updated the phrase in `AGENTS.md` to match the supplied suggestion.

## Interaction 4

**Prompt:** “let's explore the ideas, before implementation”

**Response:** Proposed exploring the project as a learning-focused wealth-management copilot before building further: start read-only with portfolio explanations, then add a deterministic rebalancing simulator, and only later explore agent orchestration with mock tools, human approval, guardrails, evaluations, and observability. Emphasized keeping investment calculations deterministic, documenting consent and account boundaries, and avoiding real trade execution. Suggested discussing the product workflow and learning goals before choosing implementation scope.