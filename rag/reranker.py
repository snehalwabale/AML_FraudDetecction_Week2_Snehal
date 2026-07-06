from rag.retriever_hybrid import hybrid_search


def rerank_documents(query: str, k: int = 5):

    documents = hybrid_search(

        query,

        k

    )

    scored = []

    query_words = set(

        query.lower().split()

    )

    for doc in documents:

        text = doc.page_content.lower()

        score = sum(

            1

            for word in query_words

            if word in text

        )

        doc.metadata["score"] = score

        scored.append(doc)

    scored.sort(

        key=lambda x: x.metadata.get(

            "score",

            0

        ),

        reverse=True

    )

    return scored