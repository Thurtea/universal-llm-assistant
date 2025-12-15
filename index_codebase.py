"""
Vector Database Indexing for AetherMUD Codebase
Creates ChromaDB index for fast semantic search
"""

import hashlib
import json
from pathlib import Path
from typing import List, Dict

import chromadb


class CodebaseIndexer:
    def __init__(
        self,
        codebase_path: str = "../aethermud-code",
        index_path: str = "./chroma_db",
        chunk_size: int = 300,
        overlap: int = 50,
    ):
        self.codebase_path = Path(codebase_path)
        self.index_path = Path(index_path)
        self.chunk_size = chunk_size
        self.overlap = overlap

        self.client = chromadb.PersistentClient(path=str(self.index_path))
        self.collection = self.client.get_or_create_collection(
            name="aethermud_code",
            metadata={"description": "AetherMUD codebase chunks"},
        )

    def chunk_file(self, file_path: Path) -> List[Dict]:
        chunks: List[Dict] = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            step = self.chunk_size - self.overlap
            for i in range(0, len(lines), step):
                chunk_lines = lines[i : i + self.chunk_size]
                chunk_text = "".join(chunk_lines)
                chunk_id = hashlib.md5(f"{file_path}:{i}".encode()).hexdigest()
                chunks.append(
                    {
                        "id": chunk_id,
                        "text": chunk_text,
                        "metadata": {
                            "file": str(file_path.relative_to(self.codebase_path.parent)),
                            "start_line": i + 1,
                            "end_line": i + len(chunk_lines),
                            "chunk_index": i // step,
                        },
                    }
                )
        except Exception as e:
            print(f"Error chunking {file_path}: {e}")
        return chunks

    def index_codebase(self):
        print("🔍 Indexing AetherMUD codebase...")
        py_files = list(self.codebase_path.rglob("*.py"))
        print(f"Found {len(py_files)} Python files")

        all_chunks: List[Dict] = []
        for file_path in py_files:
            chunks = self.chunk_file(file_path)
            all_chunks.extend(chunks)
            print(f"  Indexed: {file_path.name} ({len(chunks)} chunks)")

        batch_size = 100
        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i : i + batch_size]
            self.collection.add(
                ids=[c["id"] for c in batch],
                documents=[c["text"] for c in batch],
                metadatas=[c["metadata"] for c in batch],
            )

        print(f"✅ Indexed {len(all_chunks)} chunks from {len(py_files)} files")

        stats = {
            "total_files": len(py_files),
            "total_chunks": len(all_chunks),
            "chunk_size": self.chunk_size,
            "overlap": self.overlap,
        }
        self.index_path.mkdir(parents=True, exist_ok=True)
        with open(self.index_path / "index_stats.json", "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)
        return stats


def main():
    indexer = CodebaseIndexer()
    stats = indexer.index_codebase()

    print("\n" + "=" * 60)
    print("INDEXING COMPLETE")
    print("=" * 60)
    print(f"Files: {stats['total_files']}")
    print(f"Chunks: {stats['total_chunks']}")
    print("Index location: ./chroma_db")
    print("\nYou can now use indexed_assistant.py for fast queries!")


if __name__ == "__main__":
    main()
