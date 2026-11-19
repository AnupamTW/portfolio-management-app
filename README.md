# Educational Wealth Agent

A dependency-free Python CLI prototype for learning agent architecture in the
wealth-management domain. It is an educational example, not a financial
advisor: it does not connect to accounts, recommend personal investments, or
execute transactions.

## Run it

From the project directory:

```bash
python3 -m wealth_agent --query "How does portfolio rebalancing work?"
```

Omit `--query` to start an interactive session. Type `quit` to exit.

Run the tests:

```bash
python3 -m unittest discover -s tests -v
```

## Agent workflow

1. **Classify** the input as educational, a personalized decision, or a request
   to transact.
2. **Retrieve** relevant passages from a small, local knowledge base using
   keyword overlap.
3. **Draft** an answer from those passages. The current model is deliberately
   deterministic and local; no API key or external service is used.
4. **Apply guardrails**: personal decisions and transaction requests require
   human review, and transaction execution is always disabled.
5. **Expose the trace**: the CLI prints the intent, retrieved sources, review
   status, and workflow stages.

The knowledge base introduces account authority and consent, risk profiling,
rebalancing, robo-advisors, and human oversight. The tests cover retrieval,
decision routing, and the no-execution boundary.

## Learning path

- Replace keyword retrieval with embeddings and a vector store, while retaining
  source attribution and testing retrieval quality.
- Replace the mock drafting step with an LLM behind a typed interface; keep
  policy checks outside the model.
- Represent the stages as a LangGraph workflow and add explicit approval
  checkpoints before any consequential action.
- Add evaluation cases, structured logs, and tracing (for example Langfuse or
  LangSmith); avoid sending personal financial data to external services.
- Add a React interface only after the agent contract and approval flow are
  stable.
