import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os

from sentence_transformers import quantize_embeddings

from Models.LLMModel import LLMModel
class ChromaProcessor:

    def __init__(self):
        load_dotenv()
        self.db_name = os.getenv("DB_NAME")
        self.db_path = os.getenv("DB_PATH")
        self.model_name = os.getenv("MODEL_NAME")

    def get_all_documents(self):
        try:
            client = chromadb.PersistentClient(path=self.db_path)
            collection = client.get_collection(self.db_name)
            results = collection.get(include=["metadatas"])
            unique_sources = list({meta["source"] for meta in results["metadatas"] if "source" in meta})
            return {"Error": "","Sources":unique_sources}
        except Exception as e:
            return {"Error": str(e),"Sources":None}


    def SaveToDb(self,chunks,filename):
        PERSIST_DIR = self.db_path
        client = chromadb.PersistentClient(path=PERSIST_DIR)
        embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="llama3.2"
        )
        collection=client.get_or_create_collection(
            name="pdf_uploads",
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

    def QueryDb(self,query,document):

        PERSIST_DIR = self.db_path
        client = chromadb.PersistentClient(path=PERSIST_DIR)
        embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="llama3.2"

        )
        collection = client.get_collection(
            name="pdf_uploads",
            embedding_function=embedder
        )

        results = collection.query(
            query_texts=[query],
            n_results=3,
            where={"source": document},
        )

        if results and "documents" in results and results["documents"]:
            context = "\n\n".join(results["documents"][0])
        else:
            context = "No relevant information found in the document."

        response=self.generate_response(query,context)
        return response

    def generate_response(self,query,context):
        try:
            prompt = f"""
            Based on the following context, please answer the question.
            If you can't find the answer in the context, say so, or I don't know.
            
            Context: {context}
            
            Question: {query}
            
            Answer:
            
            """
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]

            llmmodel=LLMModel()
            return llmmodel.complete_response(messages)

        except Exception as e:
            return e
