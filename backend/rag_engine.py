import chromadb
from chromadb.utils import embedding_functions
import os
import logging
from typing import List, Dict
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Groq Client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    logger.warning("GROQ_API_KEY not found in environment variables. RAG features will fail.")

try:
    groq_client = Groq(api_key=api_key or "dummy_key")
except Exception as e:
    logger.error(f"Failed to initialize Groq client: {e}")
    groq_client = None

class RAGEngine:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Use Default (Local) Embedding Function to avoid OpenAI dependency
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        self.collection = self.client.get_or_create_collection(
            name="orbitthink_knowledge_base",
            embedding_function=self.embedding_fn
        )

    def add_documents(self, text_content: str):
        """
        Chunks the text content and adds it to the vector store.
        """
        try:
            # Simple chunking strategy
            chunk_size = 1000
            overlap = 100
            
            chunks = []
            if len(text_content) < chunk_size:
                chunks.append(text_content)
            else:
                for i in range(0, len(text_content), chunk_size - overlap):
                    chunks.append(text_content[i:i + chunk_size])
            
            if not chunks:
                 return False

            ids = [f"id_{i}" for i in range(len(chunks))]
            metadatas = [{"source": "orbitthink_website"} for _ in chunks]
            
            # Clear existing data to avoid duplicates for simplicity in this version
            try:
                existing_ids = self.collection.get()['ids']
                if existing_ids:
                    self.collection.delete(ids=existing_ids)
            except Exception:
                pass # Collection might be empty
                
            self.collection.add(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(chunks)} chunks to the knowledge base.")
            return True
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False

    def query(self, query_text: str, n_results: int = 3) -> List[str]:
        """
        Retrieves relevant documents for the query.
        """
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results['documents'][0]
        except Exception as e:
            logger.error(f"Error querying database: {e}")
            return []

    def generate_response(self, query: str) -> str:
        """
        Generates a response using the retrieved context and Groq (Llama 3).
        """
        if not groq_client:
            return "Groq API Key is missing. Please check your backend configuration."

        try:
            context_docs = self.query(query)
            context = "\n\n".join(context_docs) if context_docs else "No specific context found."
            
            system_prompt = """You are a specialized AI assistant representing OrbitThink Services.
            
            IMPORTANT: When users ask "What services do you provide?", "Who are you?", or similar questions using "you",
            they are asking about ORBITTHINK, not about you as an AI bot.
            
            You must ONLY answer questions about OrbitThink's services, team, projects, pricing, or related topics.
            Base your answers STRICTLY on the provided context below.
            
            CRITICAL RULES:
            - Questions like "What do you do?" or "What services do you offer?" = OrbitThink's services
            - Questions about "your team" = OrbitThink's team
            - Questions about "your projects/portfolio" = OrbitThink's projects
            - If the question is NOT about OrbitThink, respond: "I can only answer questions about OrbitThink Services. Please contact us for more information."
            - If the context doesn't contain the answer to an OrbitThink question, respond: "I don't have that specific information. Please contact our support team for assistance."
            - Do NOT use your general knowledge. ONLY use the provided context.
            - Keep responses brief, professional, and actionable.
            """
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
            ]
            
            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stop=None,
                stream=False
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I encountered an error processing your request."

# Singleton instance
rag_engine = RAGEngine()
