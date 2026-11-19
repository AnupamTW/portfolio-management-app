from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field

class Trade(BaseModel):
    ticker: str
    action: str  # "BUY" or "SELL"
    dollar_amount: float = Field(gt=0)

class PortfolioState(TypedDict):
    # 1. Inputs
    client_id: str
    current_holdings: dict[str, float]  # e.g., {"VTI": 120000.0, "BND": 50000.0}
    cash_balance: float

    # 2. Retrieved Context (Populated by RAG node)
    risk_profile: Optional[str]
    policy_constraints: Optional[dict]  # e.g., {"max_single_asset_pct": 0.40, "min_cash_pct": 0.05}

    # 3. Agent Proposals (Populated by LLM node)
    proposed_trades: List[Trade]
    rationale: Optional[str]

    # 4. Control & Safety Flags (Populated by Guardrails & HITL)
    guardrail_errors: List[str]
    retry_count: int
    human_approved: bool