import os

from langchain_community.vectorstores import FAISS

from rag.loaders import load_document
from rag.chunkers import chunk_document
from rag.embeddings import get_embedding_model


VECTOR_DB = "vector_db"


class VectorStore:

    def __init__(self):

        self.embeddings = get_embedding_model()

        self.db = None

        self.sources = {}

        self.load()

    def load(self):

        if os.path.exists(VECTOR_DB):

            try:

                self.db = FAISS.load_local(

                    VECTOR_DB,

                    self.embeddings,

                    allow_dangerous_deserialization=True

                )

            except Exception:

                self.db = None

    def save(self):

        if self.db:

            self.db.save_local(VECTOR_DB)

    def build(self, file_path):

        docs = load_document(file_path)

        chunks = chunk_document(docs)

        self.db = FAISS.from_documents(

            chunks,

            self.embeddings

        )

        self.sources[file_path] = len(chunks)

        self.save()

    def add(self, chunks, embeddings=None, metadata=None):

        if self.db is None:

            self.db = FAISS.from_documents(

                chunks,

                self.embeddings

            )

        else:

            self.db.add_documents(chunks)

        if metadata:

            doc_id = metadata.get("doc_id", "Unknown")

            self.sources[doc_id] = len(chunks)

        self.save()

    def similarity_search(self, query, k=5):

        if self.db is None:

            return []

        return self.db.similarity_search(

            query,

            k=k

        )

    def list_sources(self):

        result = []

        for name, count in self.sources.items():

            result.append(

                {

                    "doc_id": name,

                    "chunks": count

                }

            )

        return result

    def delete(self, doc_id):

        if doc_id in self.sources:

            del self.sources[doc_id]


vector_store = VectorStore()


if __name__ == "__main__":

    vector_store.build(

        "documents/sample.txt"

    )

    print("Vector Database Created Successfully")