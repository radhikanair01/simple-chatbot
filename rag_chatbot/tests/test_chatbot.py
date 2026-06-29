import unittest

from chatbot import ask_question


class ChatbotTests(unittest.TestCase):
    def test_answers_known_questions(self):
        answer = ask_question("What does RAG stand for?")
        self.assertTrue(answer)
        self.assertIn("RAG", answer.upper())

    def test_how_are_you_response_is_friendly(self):
        answer = ask_question("How are you?")
        self.assertTrue(answer)
        self.assertTrue(any(word in answer.lower() for word in ["great", "good", "thanks", "help"]))

    def test_thank_you_reply_is_polite(self):
        answer = ask_question("Thank you")
        self.assertTrue(answer)
        self.assertTrue(any(word in answer.lower() for word in ["welcome", "happy", "help"]))

    def test_answers_specific_topic_from_knowledge_base(self):
        answer = ask_question("What is Streamlit?")
        self.assertTrue(answer)
        self.assertIn("Streamlit", answer)

    def test_definition_questions_are_tailored(self):
        answer = ask_question("What does RAG mean?")
        self.assertTrue(answer)
        self.assertIn("Retrieval Augmented Generation", answer)

    def test_streamlit_definition_uses_updated_knowledge_entry(self):
        answer = ask_question("What is Streamlit?")
        self.assertTrue(answer)
        self.assertIn("Python library", answer)
        self.assertIn("interactive web apps", answer)

    def test_python_definition_uses_updated_knowledge_entry(self):
        answer = ask_question("What is Python?")
        self.assertTrue(answer)
        self.assertIn("general-purpose programming language", answer)

    def test_greeting_is_case_insensitive(self):
        answer = ask_question("HELLO")
        self.assertTrue(answer)
        self.assertTrue(any(word in answer.lower() for word in ["hello", "help", "hi", "mind"]))

    def test_follow_up_uses_conversation_context(self):
        context = ["What is Streamlit?", "Streamlit is a Python framework used to build interactive web applications for machine learning and data science projects quickly."]
        answer = ask_question("Tell me more about it", conversation_context=context)
        self.assertTrue(answer)
        self.assertIn("Streamlit", answer)


if __name__ == "__main__":
    unittest.main()
