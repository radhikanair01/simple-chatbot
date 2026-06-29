from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data.txt"
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "knowledge_base"

DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant. Answer using the provided context only."
