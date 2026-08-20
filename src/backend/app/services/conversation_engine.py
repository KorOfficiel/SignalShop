from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from app.services.ai_provider import get_ai_provider
from app.services.tool_gateway import (
    get_catalog,
    get_product_detail,
    check_stock,
    add_to_cart,
    create_order_from_cart
)
from app.models.customer import Customer
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.configuration import Configuration

class ConversationEngine:
    """Gère le traitement des messages et les appels aux outils métier."""

    def __init__(self):
        self.ai_provider = get_ai_provider()

    def _get_setting(self, db: Session, tenant_id, key: str, default=None):
        """Récupère une valeur de configuration pour le tenant."""
        config = db.query(Configuration).filter(
            Configuration.tenant_id == tenant_id,
            Configuration.key == key
        ).first()
        if config:
            return config.value
        return default

    def process_message(
        self,
        db: Session,
        tenant_id,
        conversation_id: str,
        customer_id: UUID,
        customer_message: str
    ) -> str:
        text = customer_message.lower().strip()

        # Récupérer les paramètres
        welcome_message = self._get_setting(db, tenant_id, "welcome_message",
            "Bonjour ! Bienvenue chez SignalShop. Comment puis-je vous aider ?")
        tone = self._get_setting(db, tenant_id, "tone", "vous")

        # ========== Logique métier simple ==========
        if "voir les chocolats" in text or "catalogue" in text or "menu" in text:
            products = get_catalog(db, tenant_id)
            if not products:
                return "Le catalogue est vide pour le moment."
            lines = ["Voici nos produits :"]
            for p in products:
                price_eur = p["base_price"] / 100
                stock = p["stock_quantity"] if p["stock_quantity"] is not None else "illimité"
                lines.append(f"- {p['name']} : {price_eur:.2f} € (stock: {stock})")
            return "\n".join(lines)

        if text.startswith("ajoute") and "au panier" in text:
            products = get_catalog(db, tenant_id)
            target = None
            for p in products:
                if p["name"].lower() in text:
                    target = p
                    break
            if not target:
                return "Je ne trouve pas ce produit. Dites-moi quel produit vous voulez."

            try:
                quantity = 1
                words = text.split()
                for i, w in enumerate(words):
                    if w.isdigit():
                        quantity = int(w)
                        break
                add_to_cart(db, tenant_id, customer_id, target["id"], quantity=quantity)
                return f"J'ai ajouté {quantity} × {target['name']} à votre panier."
            except Exception as e:
                return f"Impossible d'ajouter : {str(e)}"

        if "stock" in text:
            products = get_catalog(db, tenant_id)
            if not products:
                return "Aucun produit en catalogue."
            lines = ["Stock actuel :"]
            for p in products:
                stock = p["stock_quantity"] if p["stock_quantity"] is not None else "illimité"
                lines.append(f"- {p['name']} : {stock}")
            return "\n".join(lines)

        # ========== Salutations et message d'accueil ==========
        if "bonjour" in text or "salut" in text:
            if tone == "tu":
                welcome_message = welcome_message.replace("vous", "tu").replace("Vous", "Tu")
            return welcome_message

        # ========== Sinon, appeler l'IA (mock ou DeepSeek) ==========
        messages = [
            {"role": "system", "content": f"Tu es un assistant de vente pour SignalShop. Tu es poli et utilises le ton suivant : {tone}."},
            {"role": "user", "content": customer_message}
        ]
        return self.ai_provider.generate_response(messages)