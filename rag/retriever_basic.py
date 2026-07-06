# rag/retriever_basic.py
from rag.vectorstore import load_vectorstore

def retrieve_documents(query: str, k: int = 3):
    """
    Perform dense similarity search using the vector store.
    Returns top-k documents with metadata for citations.
    """
    db = load_vectorstore()
    results = db.similarity_search(query, k=k)

    # Attach metadata for downstream citation use
    for idx, doc in enumerate(results, start=1):
        if "doc_id" not in doc.metadata:
            doc.metadata["doc_id"] = f"vec_doc_{idx}"
        # similarity_search doesn’t return scores by default, so add a placeholder
        doc.metadata["score"] = doc.metadata.get("score", 1.0)

    return results

if __name__ == "__main__":
    docs = retrieve_documents("What is Structuring?")
    print("Retrieved Documents\n")
    for index, doc in enumerate(docs, start=1):
        print("=" * 60)
        print("Document", index)
        print("Doc ID:", doc.metadata.get("doc_id"))
        print("Score:", doc.metadata.get("score"))
        print(doc.page_content[:300])  # preview first 300 chars
