from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data.txt", "r", encoding="utf-8") as f:
    text = f.read()

chunks = [
    chunk.strip()
    for chunk in text.split("\n\n")
    if chunk.strip()
]

print(f"Found {len(chunks)} chunks")

embeddings = model.encode(chunks)

client = PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="knowledge_base"
)

for i, chunk in enumerate(chunks):

    collection.add(
        ids=[str(i)],
        documents=[chunk],
        embeddings=[embeddings[i].tolist()]
    )

print("Knowledge Base Created Successfully!")