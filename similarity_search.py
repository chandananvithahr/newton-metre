"""
CADDi-inspired similarity search for engineering drawings
Find similar parts based on shape, dimensions, features
"""
from typing import Dict, List, Optional
from PIL import Image
import numpy as np
from pathlib import Path

class DrawingSimilaritySearch:
    """
    Similarity search inspired by CADDi.
    Finds similar parts based on:
    - Shape similarity
    - Dimension similarity
    - Feature similarity
    - Material similarity
    """
    
    def __init__(self):
        self.drawing_database = []  # Store past drawings
        self.embeddings_cache = {}
    
    def generate_embedding(self, image: Image.Image, analysis: Dict) -> np.ndarray:
        """
        Generate embedding vector for similarity search.
        Combines visual features + extracted data.
        """
        # Use CLIP or similar to generate visual embedding
        # Combine with dimension/feature embeddings
        # Return combined vector
        
        # For now, simple feature-based embedding
        features = []
        
        dims = analysis.get('dimensions', {})
        if dims.get('max_diameter_mm'):
            features.append(dims['max_diameter_mm'] / 1000.0)  # Normalize
        if dims.get('length_mm'):
            features.append(dims['length_mm'] / 1000.0)
        
        # Add feature counts
        feat_list = analysis.get('features', [])
        features.append(len(feat_list))
        
        # Add material encoding
        material = analysis.get('material_on_drawing', '')
        material_hash = hash(material) % 1000 / 1000.0
        features.append(material_hash)
        
        return np.array(features)
    
    def find_similar_drawings(self, query_image: Image.Image, query_analysis: Dict, top_k: int = 5) -> List[Dict]:
        """
        Find similar drawings from database.
        Returns top K most similar with similarity scores.
        """
        query_embedding = self.generate_embedding(query_image, query_analysis)
        
        similarities = []
        for stored_drawing in self.drawing_database:
            stored_embedding = stored_drawing.get('embedding')
            if stored_embedding is not None:
                similarity = self._cosine_similarity(query_embedding, stored_embedding)
                similarities.append({
                    'drawing_id': stored_drawing.get('id'),
                    'similarity_score': similarity,
                    'metadata': stored_drawing.get('metadata', {}),
                    'cost_history': stored_drawing.get('cost_history', [])
                })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return similarities[:top_k]
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def add_to_database(self, image: Image.Image, analysis: Dict, metadata: Dict):
        """Add drawing to similarity search database."""
        embedding = self.generate_embedding(image, analysis)
        
        drawing_entry = {
            'id': len(self.drawing_database),
            'embedding': embedding,
            'analysis': analysis,
            'metadata': metadata,
            'cost_history': []
        }
        
        self.drawing_database.append(drawing_entry)
        return drawing_entry['id']
    
    def search_by_metadata(self, filters: Dict) -> List[Dict]:
        """Search drawings by metadata (material, dimensions, etc.)."""
        results = []
        
        for drawing in self.drawing_database:
            matches = True
            metadata = drawing.get('metadata', {})
            analysis = drawing.get('analysis', {})
            
            # Filter by material
            if 'material' in filters:
                if filters['material'].lower() not in str(analysis.get('material_on_drawing', '')).lower():
                    matches = False
            
            # Filter by dimension range
            if 'min_diameter' in filters:
                dims = analysis.get('dimensions', {})
                if dims.get('max_diameter_mm', 0) < filters['min_diameter']:
                    matches = False
            
            if matches:
                results.append(drawing)
        
        return results
