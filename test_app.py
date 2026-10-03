import os, tempfile, unittest

os.environ["TRUSTDESK_DB"] = tempfile.mktemp(suffix=".db")
import app

class TrustDeskTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): app.init_db()
    def test_refund_triage(self): self.assertEqual(app.triage(app.ticket_context("T-001"))["category"], "refund")
    def test_injection_is_blocked(self):
        self.assertEqual(app.make_draft(app.ticket_context("T-003"))["status"], "escalated")
    def test_retrieval_ignores_untrusted_document(self):
        self.assertNotIn("KB-ADVERSARIAL-001", [d["id"] for d in app.retrieve("refund policy")])
    def test_sensitive_action_requires_and_remembers_approval(self):
        status, action = app.recommend_refund_review("T-001", "test-refund-key")
        self.assertEqual(status, 201); self.assertEqual(action["status"], "pending_approval")
        duplicate_status, duplicate = app.recommend_refund_review("T-001", "test-refund-key")
        self.assertEqual(duplicate_status, 200); self.assertEqual(duplicate["id"], action["id"])
        status, approved = app.approve_action(action["id"], "Aman")
        self.assertEqual(status, 200); self.assertEqual(approved["status"], "executed")
    def test_seeded_evaluations_pass(self):
        self.assertEqual(app.run_evaluations()["passed"], 3)

if __name__ == "__main__": unittest.main()
