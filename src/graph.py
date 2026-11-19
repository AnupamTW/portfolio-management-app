from langgraph.graph import StateGraph, START, END
from src.state import PortfolioState, Trade
from src.rag import get_client_mandate, extract_rules_from_policy

# 1. Nodes (Functions that read state and return partial updates)
def retrieve_policy(state: PortfolioState) -> dict:
    risk_profile, policy_text = get_client_mandate(state["client_id"])
    constraints = extract_rules_from_policy(policy_text)
    return {
        "risk_profile": risk_profile,
        "policy_constraints": constraints
    }

def propose_trades(state: PortfolioState) -> dict:
    attempt = state.get("retry_count", 0) + 1
    # Mock behavior: Fail on attempt 1, succeed on attempt 2
    if attempt == 1:
        trades = [Trade(ticker="VTI", action="BUY", dollar_amount=90000.0)]
    else:
        trades = [Trade(ticker="VTI", action="BUY", dollar_amount=10000.0)]
    
    return {
        "proposed_trades": trades,
        "rationale": f"Rebalancing proposal (Attempt {attempt})",
        "retry_count": attempt
    }

def check_guardrails(state: PortfolioState) -> dict:
    # Deterministic check: Reject trades > $50k for this mock test
    errors = []
    for t in state["proposed_trades"]:
        if t.dollar_amount > 50000:
            errors.append(f"{t.ticker} trade exceeds $50k limit.")
    return {"guardrail_errors": errors}

# 2. Conditional Edge (The routing brain)
def route_after_guardrails(state: PortfolioState) -> str:
    if state["guardrail_errors"]:
        if state["retry_count"] >= 3:
            return END  # Circuit breaker: stop infinite loops
        return "propose_trades"  # Self-correction loop
    return END  # Validated (Later, this will route to Human-in-the-Loop)

# 3. Assemble the Graph
builder = StateGraph(PortfolioState)

builder.add_node("retrieve_policy", retrieve_policy)
builder.add_node("propose_trades", propose_trades)
builder.add_node("check_guardrails", check_guardrails)

builder.add_edge(START, "retrieve_policy")
builder.add_edge("retrieve_policy", "propose_trades")
builder.add_edge("propose_trades", "check_guardrails")
builder.add_conditional_edges("check_guardrails", route_after_guardrails)

graph = builder.compile()

if __name__ == "__main__":
    initial_state = {
        "client_id": "client_001",
        "current_holdings": {"VTI": 100000.0, "BND": 80000.0},
        "cash_balance": 20000.0,
        "guardrail_errors": [],
        "retry_count": 0,
        "human_approved": False
    }
    final_state = graph.invoke(initial_state)
    print("Final Trades:", final_state["proposed_trades"])
    print("Attempts:", final_state["retry_count"])