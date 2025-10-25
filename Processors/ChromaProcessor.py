import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os

from sentence_transformers import quantize_embeddings

from Models.LLMModel import LLMModel
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

    def QueryDb(self,query,document):

        PERSIST_DIR = "./pdf_store/" + document
        client = chromadb.PersistentClient(path=PERSIST_DIR)
        embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"

        )
        collection = client.get_collection(
            name="pdf_chunks",
            embedding_function=embedder
        )

        results = collection.query(
            query_texts=[query],
            n_results=3
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
