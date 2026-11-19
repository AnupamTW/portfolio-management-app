"""A small, inspectable agent workflow for learning purposes."""

from dataclasses import dataclass

from .knowledge import KnowledgeItem, retrieve


_TRANSACTION_PHRASES = (
    "execute",
    "place an order",
    "buy shares",
    "sell shares",
    "trade my",
    "transfer funds",
    "move my money",
)
_DECISION_PHRASES = (
    "should i",
    "what should i",
    "recommend",
    "my portfolio",
    "my investments",
    "buy",
    "sell",
    "trade",
    "rebalance my",
    "choose for me",
)


@dataclass(frozen=True)
class AgentResult:
    answer: str
    intent: str
    sources: tuple[str, ...]
    requires_human_review: bool
    execution_enabled: bool
    trace: tuple[str, ...]


class WealthAgent:
    """Educational-only portfolio agent; it never connects to a brokerage."""

    def run(self, query: str) -> AgentResult:
        trace = ["classify_request"]
        normalized_query = query.lower()

        if any(phrase in normalized_query for phrase in _TRANSACTION_PHRASES):
            intent = "transaction_request"
        elif any(phrase in normalized_query for phrase in _DECISION_PHRASES):
            intent = "personalized_decision"
        else:
            intent = "education"

        trace.append("retrieve_local_knowledge")
        items = retrieve(query)

        trace.append("draft_with_mock_model")
        answer = self._draft_answer(items)

        trace.append("apply_safety_guardrails")
        if intent == "transaction_request":
            answer += (
                "\n\nThis learning prototype cannot execute trades, place orders, "
                "or move money. Discretionary actions require explicit client "
                "authorization and review by an appropriately qualified human."
            )
        elif intent == "personalized_decision":
            answer += (
                "\n\nThis prototype cannot recommend a personal allocation or "
                "trade. Treat this as general education and discuss personal "
                "decisions with an appropriately qualified human advisor."
            )
        else:
            answer += (
                "\n\nEducational information only; this prototype does not provide "
                "personalized investment advice or execute transactions."
            )

        trace.append("return_for_human_review" if intent != "education" else "complete")
        return AgentResult(
            answer=answer,
            intent=intent,
            sources=tuple(item.title for item in items),
            requires_human_review=intent != "education",
            execution_enabled=False,
            trace=tuple(trace),
        )

    @staticmethod
    def _draft_answer(items: list[KnowledgeItem]) -> str:
        if not items:
            return (
                "I could not find a relevant topic in the local learning knowledge "
                "base. Try asking about account types, risk profiling, rebalancing, "
                "robo-advisors, or human oversight."
            )

        sections = "\n".join(
            f"- **{item.title}:** {item.content}" for item in items
        )
        return f"General context from the local learning notes:\n{sections}"
