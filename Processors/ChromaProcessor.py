import chromadb
from chromadb.utils import embedding_functions
class ChromaProcessor:
    def SaveToDb(self,chunks,filename):
        PERSIST_DIR = "./pdf_store/"+filename
        client = chromadb.PersistentClient(path=PERSIST_DIR)
        embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        collection=client.get_or_create_collection(
            name="pdf_chunks",
            embedding_function=embedder,
            metadata={"hnsw:space": "cosine"}
        )

        ids = [str(chunk["id"]) for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [{"source": chunk["meta_data"]} for chunk in chunks]

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )