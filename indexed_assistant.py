"""
Indexed LLM Assistant using Vector Search
Fast semantic search with ChromaDB
"""

from pathlib import Path
from typing import List, Optional, Dict

import chromadb
import ollama


class IndexedAssistant:
    def __init__(
        self,
        model: str = "qwen2.5-coder:7b",
        index_path: str = "./chroma_db",
        top_k: int = 3,
    ):
        import yaml
        from pathlib import Path
        config_path = Path(__file__).parent / "config.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        self.model = model
        self.top_k = top_k
        self.client = chromadb.PersistentClient(path=index_path)
        self.collection = self.client.get_collection(
            self.config.get("indexing", {}).get("collection_name", "universal_knowledge")
        )

    def search_codebase(self, query: str, top_k: Optional[int] = None) -> List[Dict]:
        k = top_k or self.top_k
        results = self.collection.query(query_texts=[query], n_results=k)

        chunks: List[Dict] = []
        ids = results.get("ids", [[]])[0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])
        dists = distances[0] if distances else [0] * len(ids)

        for i in range(len(ids)):
            chunks.append(
                {
                    "text": documents[i],
                    "metadata": metadatas[i],
                    "distance": dists[i],
                }
            )
        return chunks

    def query(self, question: str, top_k: Optional[int] = None, files: Optional[List[str]] = None) -> str:
        relevant_chunks = self.search_codebase(question, top_k)

        # Filter by specific files if provided
        if files:
            relevant_chunks = [
                chunk
                for chunk in relevant_chunks
                if any(file in chunk["metadata"].get("file", "") for file in files)
            ]

        context = ""
        for chunk in relevant_chunks:
            file = chunk["metadata"].get("file", "")
            start = chunk["metadata"].get("start_line", "?")
            context += f"\n\n=== {file} (lines {start}+) ===\n{chunk['text']}"

        prompt = f"""You are a helpful AI coding assistant for AetherMUD development.
AetherMUD is a Rifts-themed MUD built on Evennia framework in Python.

Relevant code context (from semantic search):
{context}

Question: {question}

Provide a clear, code-focused answer referencing specific files and lines when relevant."""

        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]

    def get_file_chunks(self, file_path: str) -> List[Dict]:
        results = self.collection.get(where={"file": file_path})
        docs = results.get("documents", [])
        metas = results.get("metadatas", [])
        rows = [
            {"text": doc, "metadata": meta}
            for doc, meta in zip(docs, metas)
        ]
        rows.sort(key=lambda x: x["metadata"].get("chunk_index", 0))
        return rows


def main():
    print("Testing Indexed Assistant...\n")
    assistant = IndexedAssistant()
    response = assistant.query("What does the Atlantean clan system do?")
    print("Response:")
    print(response)


if __name__ == "__main__":
    main()
