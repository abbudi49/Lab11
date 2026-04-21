import os
import json
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parents[1]
GUIDES_DIR = BASE_DIR / "guides"
CHROMA_DIR = BASE_DIR / "chroma_db"
INDEX_PATH = CHROMA_DIR / "index.json"


def chunk_text(text: str, chunk_size_words: int = 200, overlap: int = 30) -> List[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i : i + chunk_size_words]
        chunks.append(" ".join(chunk))
        i += chunk_size_words - overlap
    return chunks


def _read_guides() -> List[dict]:
    guides = []
    if not GUIDES_DIR.exists():
        return guides
    for p in GUIDES_DIR.iterdir():
        if p.suffix.lower() in {".txt", ".md"}:
            text = p.read_text(encoding="utf8", errors="ignore")
            guides.append({"path": str(p.name), "text": text})
        elif p.suffix.lower() == ".pdf":
            # Try minimal pdf extraction if pypdf is available
            try:
                from pypdf import PdfReader

                reader = PdfReader(str(p))
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
                guides.append({"path": str(p.name), "text": text})
            except Exception:
                # Skip unreadable PDFs
                continue
    return guides


def build_index(force: bool = False) -> None:
    """Build an index for RAG.

    Preferred path: use `chromadb` + `sentence-transformers` to create a
    persistent vector store at `chroma_db/`. If those packages are not
    available, fall back to a simple JSON index saved at `chroma_db/index.json`.
    """
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    guides = _read_guides()

    # Prepare chunks
    all_chunks = []
    for g in guides:
        chunks = chunk_text(g["text"]) if g["text"] else []
        for i, c in enumerate(chunks):
            all_chunks.append({"id": f"{g['path']}_{i}", "source": g["path"], "text": c})

    # Try to build a real chromadb vectorstore if available
    try:
        from chromadb import Client
        from chromadb.config import Settings
        from sentence_transformers import SentenceTransformer

        # If force, remove existing persisted DB so it can be rebuilt cleanly
        if force and CHROMA_DIR.exists():
            for child in CHROMA_DIR.iterdir():
                if child.is_file():
                    child.unlink()
                else:
                    # remove directories recursively
                    import shutil

                    shutil.rmtree(child)

        # Try to use PersistentClient (modern chromadb)
        from chromadb import PersistentClient
        client = PersistentClient(path=str(CHROMA_DIR))

        # get or create collection
        collection = client.get_or_create_collection(name="trip_guides")

        model = SentenceTransformer("all-MiniLM-L6-v2")
        texts = [c["text"] for c in all_chunks]
        ids = [c["id"] for c in all_chunks]
        metadatas = [{"source": c["source"]} for c in all_chunks]

        # Compute embeddings (small model)
        embeddings = model.encode(texts, show_progress_bar=False).tolist()

        # If force, delete and recreate collection to ensure clean state
        if force:
            try:
                client.delete_collection(name="trip_guides")
                collection = client.create_collection(name="trip_guides")
            except Exception:
                collection = client.get_or_create_collection(name="trip_guides")

        # Add documents with embeddings
        if texts:
            collection.add(documents=texts, metadatas=metadatas, ids=ids, embeddings=embeddings)

        print(f"ChromaDB: indexed {len(texts)} chunks from {len(guides)} files.")
        return
    except Exception as e:
        import traceback

        print("ChromaDB mode failed, falling back to JSON index. Error:")
        traceback.print_exc()

    # JSON fallback
    if INDEX_PATH.exists() and not force:
        # Don't rebuild if already present
        print("JSON index exists; skipping rebuild.")
        return

    with INDEX_PATH.open("w", encoding="utf8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"Indexed {len(all_chunks)} chunks from {len(guides)} files (JSON fallback).")


def ensure_index() -> None:
    # Check if ChromaDB exists (directory not empty) or JSON index exists
    has_chroma = False
    if CHROMA_DIR.exists():
        # Look for typical sqlite or other files created by chroma
        if any(CHROMA_DIR.iterdir()):
            has_chroma = True

    if not has_chroma and (not INDEX_PATH.exists() or INDEX_PATH.stat().st_size == 0):
        print("No index found. Building index...")
        build_index(force=True)


def search_guides(query: str, n_results: int = 3) -> List[str]:
    """Return top matching text chunks using ChromaDB or simple fallback."""
    ensure_index()

    # Try ChromaDB first
    try:
        from chromadb import PersistentClient
        from sentence_transformers import SentenceTransformer

        # Standard persistent client
        client = PersistentClient(path=str(CHROMA_DIR))
        collection = client.get_collection(name="trip_guides")
        
        model = SentenceTransformer("all-MiniLM-L6-v2")
        query_embeddings = model.encode([query], show_progress_bar=False).tolist()

        results = collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results
        )
        if results and results["documents"] and results["documents"][0]:
            return results["documents"][0]
    except Exception as e:
        # If ChromaDB fails, try falling back to JSON
        # print(f"Chroma search failed: {e}")
        pass

    # JSON fallback
    try:
        with INDEX_PATH.open(encoding="utf8") as f:
            chunks = json.load(f)
    except Exception:
        return []

    q_words = set(query.lower().split())
    scored = []
    for c in chunks:
        text_words = set(c["text"].lower().split())
        score = len(q_words & text_words)
        scored.append((score, c))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = [c["text"] for s, c in scored if s > 0][:n_results]
    
    # If no overlap matches, return the top n raw chunks (best-effort)
    if not results:
        return [c["text"] for c in chunks[:n_results]]
    return results


if __name__ == "__main__":
    build_index(force=True)
