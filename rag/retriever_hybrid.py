from rag.vectorstore import vector_store

from rbac.filter import apply_role_filter
from rbac.validator import validate_documents
from rbac.audit import log_rbac_event


import re



# =====================================================
# Keyword Search
# =====================================================


def keyword_search(
        query,
        documents
):

    """
    Simple AML keyword relevance scoring.
    """

    query_words = set(

        re.findall(

            r"\w+",

            query.lower()

        )

    )


    scored=[]


    for doc in documents:


        content = doc.page_content.lower()


        words = set(

            re.findall(

                r"\w+",

                content

            )

        )


        overlap = len(

            query_words.intersection(words)

        )


        scored.append(

            {

                "document":doc,

                "keyword_score":overlap

            }

        )


    scored.sort(

        key=lambda x:x["keyword_score"],

        reverse=True

    )


    return scored





# =====================================================
# Hybrid Retrieval
# =====================================================


def hybrid_search(

    query,

    top_k=5,

    role="analyst"

):

    """
    Hybrid AML retrieval.

    Combines:

    1. Vector similarity
    2. Keyword relevance
    3. RBAC filtering
    """



    # -------------------------------
    # Semantic Retrieval
    # -------------------------------


    semantic_docs = vector_store.similarity_search(

        query,

        k=top_k*3

    )



    # -------------------------------
    # Keyword Retrieval
    # -------------------------------


    keyword_docs = keyword_search(

        query,

        semantic_docs

    )



    # -------------------------------
    # Combine Ranking
    # -------------------------------


    ranked=[]


    for item in keyword_docs:


        doc=item["document"]


        score=item["keyword_score"]


        ranked.append(

            {

                "document":doc,

                "score":score

            }

        )



    ranked.sort(

        key=lambda x:x["score"],

        reverse=True

    )



    documents=[

        item["document"]

        for item in ranked

    ]



    # -------------------------------
    # RBAC Security
    # -------------------------------


    documents = apply_role_filter(

        documents,

        role

    )



    documents = validate_documents(

        documents,

        role

    )



    # -------------------------------
    # Audit
    # -------------------------------


    log_rbac_event(

        role,

        query,

        documents

    )



    # -------------------------------
    # Response Trace
    # -------------------------------


    results=[]


    for doc in documents[:top_k]:


        results.append(

            {

                "content":

                doc.page_content,


                "source":

                doc.metadata.get(

                    "source",

                    "unknown"

                ),


                "retrieval_method":

                "hybrid",


                "confidence":

                0.85


            }

        )



    return results