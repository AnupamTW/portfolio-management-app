"""Small, local knowledge base used to demonstrate retrieval."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class KnowledgeItem:
    title: str
    content: str
    tags: tuple[str, ...]


KNOWLEDGE_BASE = (
    KnowledgeItem(
        title="Self-directed and discretionary accounts",
        content=(
            "In a self-directed account, the investor makes investment decisions. "
            "In a discretionary account, an authorized manager may make decisions "
            "within an agreed mandate. Discretionary management requires explicit "
            "client authorization and ongoing oversight."
        ),
        tags=("self-directed", "discretionary", "consent", "authorization", "oversight"),
    ),
    KnowledgeItem(
        title="Risk profiling",
        content=(
            "Risk profiling considers an investor's goals, time horizon, financial "
            "capacity for loss, and comfort with volatility. A profile is a starting "
            "point for a conversation, not a guarantee of outcomes or a standalone "
            "instruction to trade."
        ),
        tags=("risk", "profile", "goals", "horizon", "loss", "volatility"),
    ),
    KnowledgeItem(
        title="Portfolio rebalancing",
        content=(
            "Rebalancing brings a portfolio back toward a chosen target allocation "
            "after market movements change its mix. A learning exercise can compare "
            "current and target weights and discuss costs, taxes, and constraints; "
            "it should not place trades without suitable authorization and review."
        ),
        tags=("portfolio", "rebalance", "rebalancing", "allocation", "weights", "trade"),
    ),
    KnowledgeItem(
        title="Robo-advisors",
        content=(
            "Robo-advisors use software to support activities such as onboarding, "
            "risk questionnaires, portfolio construction, or monitoring. Their "
            "services, human involvement, and decision authority vary, so the "
            "account terms and client permissions matter."
        ),
        tags=("robo-advisor", "robo", "automation", "monitoring", "software"),
    ),
    KnowledgeItem(
        title="Human oversight and guardrails",
        content=(
            "A responsible investment workflow should make its limits clear, use "
            "approved information, validate outputs, preserve an audit trail, and "
            "route consequential or uncertain decisions to an authorized human. "
            "Client consent should be specific and recorded before discretionary "
            "actions."
        ),
        tags=("human", "oversight", "guardrail", "consent", "audit", "validation"),
    ),
)


_STOP_WORDS = {
    "a", "an", "and", "are", "about", "can", "do", "does", "for", "how", "i",
    "in", "is", "it", "me", "of", "on", "or", "should", "the", "to", "what",
    "when", "with", "would", "my",
}


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in _STOP_WORDS
    }


def retrieve(query: str, limit: int = 3) -> list[KnowledgeItem]:
    """Return the most relevant local notes using simple lexical overlap."""
    query_tokens = _tokens(query)
    if not query_tokens:
        return []

    ranked = []
    for item in KNOWLEDGE_BASE:
        searchable = _tokens(f"{item.title} {item.content} {' '.join(item.tags)}")
        score = len(query_tokens & searchable)
        if score:
            ranked.append((score, item))

    ranked.sort(key=lambda result: -result[0])
    return [item for _, item in ranked[:limit]]
