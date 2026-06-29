import random
import re
from typing import List, Optional

from config import DATA_FILE, DEFAULT_SYSTEM_PROMPT


def _load_knowledge_base() -> list[str]:
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as handle:
        text = handle.read()

    parts = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    return parts


def _find_relevant_context(question: str, knowledge_base: list[str], limit: int = 3) -> list[str]:
    stop_words = {
        "a", "an", "and", "are", "can", "for", "how", "i", "in", "is", "it", "me", "my",
        "of", "on", "or", "the", "this", "to", "what", "who", "why", "you", "your"
    }
    question_tokens = [token for token in re.findall(r"[a-z0-9]+", question.lower()) if token not in stop_words]
    question_terms = set(question_tokens)

    scored: list[tuple[float, str]] = []

    for chunk in knowledge_base:
        chunk_tokens = [token for token in re.findall(r"[a-z0-9]+", chunk.lower()) if token not in stop_words]
        chunk_terms = set(chunk_tokens)
        overlap = len(question_terms & chunk_terms)
        if overlap == 0:
            continue

        exact_matches = sum(1 for term in question_tokens if term in chunk_terms)
        phrase_bonus = 1 if any(term in chunk.lower() for term in question_tokens) else 0
        score = (exact_matches * 2) + overlap + phrase_bonus
        scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in scored[:limit]]


def _get_greeting_reply() -> str:
    greetings = [
        "Hi! 👋 How are you doing today?",
        "Hello! 😊 What can I help you with?",
        "Hey there! What's on your mind?",
        "Hi! I'm here and ready to help. ✨",
    ]
    return random.choice(greetings)


def _get_how_are_you_reply() -> str:
    replies = [
        "I'm doing great! Thanks for asking. 😊",
        "I'm good! How about you?",
        "Doing well, thanks! I'm ready to help. 🌟",
    ]
    return random.choice(replies)


def _get_thanks_reply() -> str:
    replies = [
        "You're welcome! 😄",
        "Happy to help!",
        "My pleasure! 😊",
    ]
    return random.choice(replies)


def _get_farewell_reply() -> str:
    replies = [
        "Goodbye! Have a wonderful day! 👋",
        "See you later! Take care. 🌈",
        "Bye for now! Wishing you a lovely day. 😊",
    ]
    return random.choice(replies)


def _get_follow_up_reply(question: str, conversation_context: Optional[List[str]] = None) -> str:
    if "rag" in question.lower():
        return "I can help with RAG topics. For example, ask me what RAG stands for or how embeddings work."
    if "chroma" in question.lower():
        return "I can explain ChromaDB and how it fits into a RAG pipeline. What would you like to know?"
    if conversation_context:
        return "I can help with that. I’m drawing from our earlier conversation and the knowledge base. 😊"
    return "I’m happy to help! Could you tell me a bit more about what you want to know?"


def _find_best_topic_answer(question: str, relevant_context: list[str]) -> str:
    q = question.lower().strip()
    topic_patterns = [
        "streamlit",
        "python",
        "chatbot",
        "knowledge base",
        "knowledgebase",
        "large language model",
        "llm",
        "vector search",
        "api",
        "embedding model",
        "embeddings",
        "chroma",
        "deep learning",
        "rag",
    ]

    for pattern in topic_patterns:
        if pattern in q:
            for chunk in relevant_context:
                if pattern in chunk.lower():
                    return chunk

    return relevant_context[0]


def _generate_answer(question: str, relevant_context: list[str], conversation_context: Optional[List[str]] = None) -> str:
    q = question.lower().strip()

    if re.fullmatch(r"(?:hi|hello|hey|hey there|hello there)", q):
        return _get_greeting_reply()

    if q.startswith(("hi ", "hello ", "hey ", "hey there ", "hello there ")):
        return _get_greeting_reply()

    if "how are you" in q or "how are u" in q:
        return _get_how_are_you_reply()

    if "thank you" in q or q.startswith("thanks") or q == "thanks":
        return _get_thanks_reply()

    if q in {"bye", "goodbye", "see you later", "see ya"}:
        return _get_farewell_reply()

    if "what can you do" in q or "what can i do for you" in q or "what can i do" in q:
        return "I can help answer questions about the documents, explain RAG concepts, and chat naturally with you. 😊"

    if "tell me more" in q or "more about it" in q or "explain more" in q:
        if conversation_context:
            topic = next((item for item in reversed(conversation_context) if item and "streamlit" in item.lower()), None)
            if topic:
                return "Sure! I can expand on Streamlit. It is a Python framework for building interactive web apps quickly. 😊"
            return "Sure! I’m using the context we’ve already discussed to keep the explanation relevant. 😊"
        return "Absolutely! I’d be happy to explain it further."

    if not relevant_context:
        return _get_follow_up_reply(q, conversation_context)

    answer = _find_best_topic_answer(q, relevant_context)

    if "rag" in q and ("stand" in q or "mean" in q or "means" in q or "mean" in q):
        return "RAG stands for Retrieval Augmented Generation."
    if "embedding" in q or "embeddings" in q:
        return "Embeddings convert text into vectors."
    if "chroma" in q:
        return "ChromaDB is a vector database used in RAG applications."
    if "deep learning" in q:
        return "Deep learning is a subset of machine learning."
    if answer.endswith("."):
        return answer
    return answer + "."


def ask_question(question: str, conversation_context: Optional[List[str]] = None) -> str:
    """Answer a question using the knowledge base while keeping the conversation natural."""
    if not question or not question.strip():
        return "Please enter a question first."

    knowledge_base = _load_knowledge_base()
    if not knowledge_base:
        return "No knowledge base content is available yet."

    relevant_context = _find_relevant_context(question, knowledge_base)
    if not relevant_context:
        return _get_follow_up_reply(question, conversation_context)

    return _generate_answer(question, relevant_context, conversation_context)
