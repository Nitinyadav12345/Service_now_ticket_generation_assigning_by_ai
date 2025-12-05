"""
Vector database service for RAG (Retrieval Augmented Generation)
Uses ChromaDB for similarity search
"""
import logging
from typing import List, Dict, Optional
import openai
from app.config import settings

logger = logging.getLogger(__name__)

# Try to import ChromaDB
try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logger.warning("ChromaDB not installed. RAG features will be disabled.")

# Configure OpenAI for embeddings
openai.api_key = settings.openai_api_key
if hasattr(settings, 'openai_api_base') and settings.openai_api_base:
    openai.base_url = settings.openai_api_base


class VectorService:
    """Service for vector embeddings and similarity search"""
    
    def __init__(self):
        self.embedding_model = settings.openai_embedding_model
        self.client = None
        self.collection = None
        
        if CHROMADB_AVAILABLE:
            try:
                # Initialize ChromaDB client
                self.client = chromadb.Client(ChromaSettings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory="./chroma_db"
                ))
                
                # Get or create collection
                self.collection = self.client.get_or_create_collection(
                    name="jira_stories",
                    metadata={"description": "Jira story embeddings for RAG"}
                )
                
                logger.info("ChromaDB initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize ChromaDB: {e}")
                self.client = None
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI"""
        try:
            response = openai.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return []
    
    def add_story(
        self,
        issue_key: str,
        title: str,
        description: str,
        estimated_points: int,
        actual_points: Optional[int] = None,
        completion_time_days: Optional[float] = None
    ):
        """Add story to vector database"""
        if not self.collection:
            logger.warning("ChromaDB not available, skipping add_story")
            return
        
        try:
            # Combine title and description for embedding
            text = f"{title}\n\n{description}"
            
            # Generate embedding
            embedding = self.generate_embedding(text)
            
            if not embedding:
                logger.error(f"Failed to generate embedding for {issue_key}")
                return
            
            # Add to collection
            self.collection.add(
                ids=[issue_key],
                embeddings=[embedding],
                documents=[text],
                metadatas=[{
                    "title": title,
                    "estimated_points": estimated_points,
                    "actual_points": actual_points or estimated_points,
                    "completion_time_days": completion_time_days or 0
                }]
            )
            
            logger.info(f"Added story {issue_key} to vector DB")
            
        except Exception as e:
            logger.error(f"Error adding story to vector DB: {e}")
    
    def find_similar_stories(
        self,
        title: str,
        description: str,
        top_k: int = 5
    ) -> List[Dict]:
        """Find similar stories using vector similarity search"""
        if not self.collection:
            logger.warning("ChromaDB not available, returning empty results")
            return []
        
        try:
            # Combine title and description
            text = f"{title}\n\n{description}"
            
            # Generate embedding for query
            query_embedding = self.generate_embedding(text)
            
            if not query_embedding:
                logger.error("Failed to generate query embedding")
                return []
            
            # Query collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            # Format results
            similar_stories = []
            if results and results['ids'] and len(results['ids']) > 0:
                for i, issue_key in enumerate(results['ids'][0]):
                    metadata = results['metadatas'][0][i]
                    distance = results['distances'][0][i] if 'distances' in results else 0
                    
                    # Convert distance to similarity score (0-1)
                    similarity_score = 1 - (distance / 2)  # Cosine distance to similarity
                    
                    similar_stories.append({
                        "issue_key": issue_key,
                        "title": metadata.get("title", ""),
                        "estimated_points": metadata.get("estimated_points", 0),
                        "actual_points": metadata.get("actual_points", 0),
                        "completion_time_days": metadata.get("completion_time_days", 0),
                        "similarity_score": round(similarity_score, 3)
                    })
            
            logger.info(f"Found {len(similar_stories)} similar stories")
            return similar_stories
            
        except Exception as e:
            logger.error(f"Error finding similar stories: {e}")
            return []
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the vector collection"""
        if not self.collection:
            return {"status": "unavailable", "count": 0}
        
        try:
            count = self.collection.count()
            return {
                "status": "available",
                "count": count,
                "name": self.collection.name
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"status": "error", "count": 0}
