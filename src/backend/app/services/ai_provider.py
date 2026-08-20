from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import os
from openai import OpenAI
from app.core.config import settings

class AIProvider(ABC):
    """Interface abstraite pour les fournisseurs IA."""

    @abstractmethod
    def generate_response(self, messages: List[Dict[str, str]], tools: List[Dict[str, Any]] = None) -> str:
        pass

class MockAIProvider(AIProvider):
    """Fournisseur IA simulé pour le développement."""

    def generate_response(self, messages: List[Dict[str, str]], tools: List[Dict[str, Any]] = None) -> str:
        user_messages = [msg["content"] for msg in messages if msg["role"] == "user"]
        if not user_messages:
            return "Je n'ai pas compris votre demande. Pouvez-vous reformuler ?"
        last_user_message = user_messages[-1].lower()

        if "bonjour" in last_user_message or "salut" in last_user_message:
            return "Bonjour ! Je suis l'assistant SignalShop. Que puis-je faire pour vous ? Vous pouvez consulter le menu, commander, ou demander à parler à quelqu'un."
        elif "menu" in last_user_message:
            return "Voici les catégories disponibles : Chocolats. Vous pouvez me demander 'voir les chocolats'."
        elif "commander" in last_user_message or "achat" in last_user_message:
            return "Bien sûr, que souhaitez-vous commander ? Dites-moi le produit et la quantité."
        elif "chocolat" in last_user_message:
            return "Nous avons du Chocolat Noir. Souhaitez-vous le commander ?"
        elif "parler à quelqu'un" in last_user_message or "humain" in last_user_message:
            return "Je préviens un membre de l'équipe. Un instant..."
        elif "merci" in last_user_message:
            return "Je vous en prie ! Puis-je vous aider pour autre chose ?"
        else:
            return "Je ne suis pas sûr de comprendre. Pouvez-vous préciser ? Vous pouvez aussi consulter le menu."

class DeepSeekProvider(AIProvider):
    """Fournisseur IA utilisant l'API DeepSeek (compatible OpenAI)."""

    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )

    def generate_response(self, messages: List[Dict[str, str]], tools: List[Dict[str, Any]] = None) -> str:
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            # En cas d'erreur, on renvoie un message simple
            return "Désolé, je rencontre un problème technique. Pouvez-vous reformuler ou demander à parler à quelqu'un ?"

# Factory pour obtenir le fournisseur
def get_ai_provider():
    if settings.deepseek_api_key:
        return DeepSeekProvider(settings.deepseek_api_key)
    return MockAIProvider()