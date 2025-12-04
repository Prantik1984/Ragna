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
            model_name="all-MiniLM-L6-v2"
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
            model_name="all-MiniLM-L6-v2"

        )
        collection = client.get_collection(
            name="pdf_uploads",
            embedding_function=embedder
        )

        results = collection.query(
            query_texts=[query],
            n_results=5,
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
            user_msg = {
                "role": "user",
                "content": f"""
            You are given some context from documents and a user question.

            CONTEXT:
            \"\"\" 
            {context}
            \"\"\"

            QUESTION:
            {query}

            INSTRUCTIONS:
            - Answer the question using ONLY the information in CONTEXT.
            - It is allowed to paraphrase or combine sentences from the context.
            - If the answer cannot be reasonably inferred from the context, reply exactly:
              "I don't know based on the provided documents."
            - Do not use any outside knowledge.
            - Do not guess beyond what can be inferred from the context..

            Answer:
            """,
            }

            system_msg = {
                "role": "system",
                "content": (
                    "You are a helpful assistant that answers questions based ONLY on the provided context.\n"
                    "You may rephrase, summarize, or logically infer answers as long as they are clearly supported by the context.\n"
                    "If the answer cannot be reasonably inferred from the context, say:"
                    "\"I don't know based on the provided documents.\"\n"
                    "- Do NOT use any outside knowledge.\n"
                    "- Do NOT invent facts."
                ),
            }

            messages = [
                system_msg,
                user_msg,
            ]

            llmmodel=LLMModel()
            return llmmodel.complete_response(messages)

        except Exception as e:
            return e
