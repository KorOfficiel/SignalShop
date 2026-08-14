18_API.md
ANNEXE : Correspondance outils IA / API 


Outil IA
Méthode HTTP
Route API
Paramètres principaux
Réponse
get_catalog
GET
/api/v1/products?active=true
tenant_id (contexte)
Liste produits actifs + variantes
get_product
GET
/api/v1/products/{id}
id
Détail produit
get_variants
GET
/api/v1/variants?product_id=
product_id
Liste variantes actives
check_stock
GET
/api/v1/inventory/check
product_id, variant_id, quantity
Disponibilité, stock restant
check_availability
GET
/api/v1/schedules/check
date, time
Créneaux disponibles / alternatives
get_delivery_options
GET
/api/v1/delivery-zones/active
adresse (zone)
Zones et tarifs
calculate_cart
POST
/api/v1/cart/calculate
cart_id ou items
Total détaillé
create_cart
POST
/api/v1/cart
customer_id
Cart ID
update_cart
PATCH
/api/v1/cart/{id}
item_id, quantity, variant, options
Panier mis à jour
remove_cart_item
DELETE
/api/v1/cart/{id}/items/{iid}
item_id
Panier mis à jour
create_order
POST
/api/v1/orders
cart_id, adresse, créneau
Commande créée
get_order
GET
/api/v1/orders/{id}
order_id
Détail commande
cancel_order
POST
/api/v1/orders/{id}/cancel
order_id
Statut annulé
request_human
POST
/api/v1/conversations/{id}/handoff
conversation_id
État HUMAN_WAITING


1. Principes
API REST sous /api/v1.
Authentification par JWT pour dashboard.
Toutes les entrées validées.
Réponses structurées en JSON.
Erreurs avec code interne, sans données sensibles.
Idempotence pour les opérations critiques.
2. Principales routes
Domaine
Routes
Authentification
/auth/login, /auth/logout, /auth/me
Produits
/products, /products/{id}
Catégories
/categories, /categories/{id}
Variantes
/variants
Commandes
/orders, /orders/{id}
Clients
/customers, /customers/{id}
Conversations
/conversations, /conversations/{id}, messages, handoff, reprise IA
Créneaux
/schedules, /schedules/{id}
Stock
/inventory, /inventory/{product_id}
Livraison
/delivery-zones
Paramètres
/settings
Notifications
/notifications, /notifications/{id}/read
Système
/system/health, /system/status

3. Règles
Toute opération critique est transactionnelle.
Toute réponse d’erreur est normalisée.
Les routes sont protégées par rôle.
Les IDs sont UUID.
Les montants sont des entiers de centimes.
4. Erreurs
400 validation.
401 non authentifié.
403 non autorisé.
404 introuvable.
409 conflit (stock, créneau).
422 données invalides.
503 service indisponible.
5. Tests
Validation des entrées.
Authentification et autorisations.
Réponses d’erreur.
Idempotence.
