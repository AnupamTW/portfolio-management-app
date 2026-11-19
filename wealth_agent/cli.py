"""Command-line entry point for the educational agent."""

import argparse

from .agent import AgentResult, WealthAgent


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ask the educational wealth-management agent a question."
    )
    parser.add_argument(
        "--query",
        help="Question to answer. Omit to start an interactive session.",
    )
    args = parser.parse_args()
    agent = WealthAgent()

    if args.query:
        _print_result(agent.run(args.query))
        return

    print("Educational Wealth Agent (type 'quit' to exit)")
    while True:
        try:
            query = input("\nYou: ").strip()
        except EOFError:
            break
        if query.lower() in {"quit", "exit"}:
            break
        if query:
            _print_result(agent.run(query))


def _print_result(result: AgentResult) -> None:
    print(f"\nAgent: {result.answer}")
    print(f"\nIntent: {result.intent}")
    print(f"Human review required: {'yes' if result.requires_human_review else 'no'}")
    print(f"Transaction execution enabled: {'yes' if result.execution_enabled else 'no'}")
    print(f"Sources: {', '.join(result.sources) if result.sources else 'none'}")
    print(f"Workflow: {' -> '.join(result.trace)}")
