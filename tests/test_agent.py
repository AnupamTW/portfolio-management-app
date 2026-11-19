import unittest

from wealth_agent import WealthAgent
from wealth_agent.knowledge import retrieve


class KnowledgeRetrievalTests(unittest.TestCase):
    def test_retrieves_rebalancing_topic(self) -> None:
        items = retrieve("How does portfolio rebalancing work?")

        self.assertTrue(items)
        self.assertEqual(items[0].title, "Portfolio rebalancing")

    def test_returns_no_topics_for_unrelated_query(self) -> None:
        self.assertEqual(retrieve("What is the weather today?"), [])


class AgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = WealthAgent()

    def test_educational_question_uses_local_context_without_review(self) -> None:
        result = self.agent.run("How does portfolio rebalancing work?")

        self.assertEqual(result.intent, "education")
        self.assertFalse(result.requires_human_review)
        self.assertIn("Portfolio rebalancing", result.sources)
        self.assertFalse(result.execution_enabled)

    def test_personal_decision_is_routed_to_human(self) -> None:
        result = self.agent.run("Should I rebalance my portfolio now?")

        self.assertEqual(result.intent, "personalized_decision")
        self.assertTrue(result.requires_human_review)
        self.assertIn("qualified human advisor", result.answer)

    def test_transaction_request_is_never_executed(self) -> None:
        result = self.agent.run("Please place an order to buy shares.")

        self.assertEqual(result.intent, "transaction_request")
        self.assertTrue(result.requires_human_review)
        self.assertFalse(result.execution_enabled)
        self.assertIn("cannot execute trades", result.answer)


if __name__ == "__main__":
    unittest.main()
