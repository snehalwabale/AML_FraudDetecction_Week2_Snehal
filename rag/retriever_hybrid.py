from rag.vectorstore import vector_store


def hybrid_search(query: str, k: int = 5):

    documents = vector_store.similarity_search(

        query,

        k=k

    )

    return documents