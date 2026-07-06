from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings

load_dotenv()

_embedding_model = None


def get_embedding_model():

    global _embedding_model

    if _embedding_model is None:

        _embedding_model = OpenAIEmbeddings(

            model="text-embedding-3-small"

        )

    return _embedding_model


def embed_chunks(chunks):

    embeddings = get_embedding_model()

    return embeddings.embed_documents(

        [

            chunk.page_content

            for chunk in chunks

        ]

    )


def embed_documents(documents):

    embeddings = get_embedding_model()

    return embeddings.embed_documents(

        [

            doc.page_content

            for doc in documents

        ]

    )


def embed_query(query):

    embeddings = get_embedding_model()

    return embeddings.embed_query(query)