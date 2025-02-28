from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import json
import os
from pathlib import Path
from typing import List, Dict, Tuple

class DocumentIndexer:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.docs = {}
        self.vectors = None
        self.all_docs = []
        
        # Ensure docs directory exists
        self.docs_dir = Path("data/docs")
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        
        self.load_documents()

    def load_documents(self):
        """Load all CDP documentation from JSON files"""
        if not os.path.exists(self.docs_dir):
            print("No documents directory found. Creating empty index.")
            return

        for filename in os.listdir(self.docs_dir):
            if filename.endswith('_docs.json'):
                cdp = filename.replace('_docs.json', '')
                try:
                    with open(os.path.join(self.docs_dir, filename), 'r', encoding='utf-8') as f:
                        self.docs[cdp] = json.load(f)
                except Exception as e:
                    print(f"Error loading {filename}: {str(e)}")
                    continue

        # Create a flat list of all documents
        self.all_docs = []
        for cdp, articles in self.docs.items():
            for article in articles:
                self.all_docs.append({
                    'cdp': cdp,
                    'title': article['title'],
                    'content': article['content'],
                    'url': article['url']
                })

        # Create TF-IDF vectors if we have documents
        if self.all_docs:
            texts = [doc['content'] for doc in self.all_docs]
            self.vectors = self.vectorizer.fit_transform(texts)

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for relevant documentation based on query"""
        if not self.all_docs:
            return []
            
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.vectors).flatten()
        
        # Get top-k most similar documents
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            doc = self.all_docs[idx]
            results.append({
                'cdp': doc['cdp'],
                'title': doc['title'],
                'content': doc['content'],
                'url': doc['url'],
                'similarity': similarities[idx]
            })
            
        return results 