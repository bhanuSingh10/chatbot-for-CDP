from typing import Dict
from .knowledge_base import CDPKnowledgeBase

class CDPChatbot:
    def __init__(self):
        self.knowledge_base = CDPKnowledgeBase()
        
    def answer_question(self, question: str) -> Dict:
        """Process user question and generate response"""
        response = self.knowledge_base.search(question)
        formatted_response = self.knowledge_base.format_response(response)
        
        return {
            'answer': formatted_response,
            'relevant_docs': []  # Keeping this for API compatibility
        } 