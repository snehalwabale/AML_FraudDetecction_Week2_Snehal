# rag/retriever_bm25.py
from langchain_community.retrievers import BM25Retriever
from rag.loaders import load_document
from rag.chunkers import chunk_document

def build_bm25(file_path: str = "documents/sample.txt", k: int = 3):
    """
    Build a BM25 retriever from the given file.
    Default: sample.txt, top-k = 3.
    """
    documents = load_document(file_path)
    chunks = chunk_document(documents)

    retriever = BM25Retriever.from_documents(chunks)
    retriever.k = k
    return retriever

def retrieve_documents(query: str, file_path: str = "documents/sample.txt", k: int = 3):
    """
    Retrieve documents using BM25 lexical search.
    Adds doc_id and score metadata for citations.
    """
    retriever = build_bm25(file_path=file_path, k=k)
    results = retriever.invoke(query)

    # Attach metadata for downstream citation use
    for idx, doc in enumerate(results, start=1):
        if "doc_id" not in doc.metadata:
            doc.metadata["doc_id"] = f"bm25_doc_{idx}"
        if "score" not in doc.metadata:
            doc.metadata["score"] = len(doc.page_content)  # simple heuristic

    return results

if __name__ == "__main__":
    docs = retrieve_documents("Suspicious Activity Report")
    print("BM25 Retrieval\n")
    for index, doc in enumerate(docs, start=1):
        print("=" * 60)
        print("Document", index)
        print("Doc ID:", doc.metadata.get("doc_id"))
        print("Score:", doc.metadata.get("score"))
        print(doc.page_content[:300])  # preview first 300 chars
