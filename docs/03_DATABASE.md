03_DATABASE.md
1. Principes
PostgreSQL est la source de vérité.
Toutes les tables métier portent tenant_id pour isolation multitenant.
Les identifiants internes sont UUID non prédictibles.
Les montants sont stockés en entiers de centimes.
Les dates/heures sont stockées en UTC, avec timezone d’entreprise configurable.
Les opérations critiques sont transactionnelles.
Les données sensibles sont chiffrées au repos selon leur catégorie.
2. Entités principales
2.1 Tenant
Représente une entreprise isolée.
Champs : identifiant, nom, timezone, devise, paramètres de conservation.
2.2 User
Compte dashboard.
Champs : identifiant, tenant, email, mot de passe haché, rôle.
Rôles : OWNER, ADMIN, MANAGER, STAFF.
2.3 Customer
Client interne sans compte externe.
Lié au numéro Signal par un hash.
Champs : identifiant, tenant, hash Signal, préférences éventuelles.
2.4 Conversation
Identifie la conversation avec un client.
Champs : identifiant, tenant, customer, état IA/humain, timer.
Ne stocke par défaut que des métadonnées de messages.
2.5 MessageMetadata
Métadonnées de message, sans contenu brut par défaut.
Champs : identifiant, conversation, expéditeur, timestamp, hash, longueur.
2.6 Category
Catégorie de produits.
Champs : nom, description, image, position, active.
2.7 Product
Produit.
Champs : nom, description, image, catégorie, prix de base, unité, mode de stock, seuil d’alerte, statut, position, disponibilité.
2.8 Variant
Variante d’un produit.
Champs : nom, description, supplément ou prix fixe, stock, référence, image, disponibilité.
2.9 OptionDefinition
Option configurable sur un produit.
Types : choix unique, choix multiple, texte, nombre, oui/non.
Champs : nom, type, choix possibles, requis.
2.10 Cart
Panier actif.
Champs : identifiant, tenant, client, état, dates.
2.11 CartItem
Ligne de panier.
Champs : produit, variante, quantité, options, prix unitaire, total.
2.12 Order
Commande confirmée.
Champs : client, statut, montant total, frais livraison, adresse, créneau, dates.
2.13 OrderItem
Ligne de commande figée au moment de la commande.
2.14 TimeSlot
Créneau horaire.
Champs : début, fin, capacité, nombre réservé, actif.
2.15 DeliveryZone
Zone de livraison.
Champs : nom, tarif, minimum éventuel, activation.
2.16 HumanHandoff
Prise en main humaine.
Champs : état, demandé le, pris le, terminé le, timer.
2.17 AIState
État de conversation pour l’IA.
Champs : identifiant conversation, état, contexte minimal.
AIState stocke également l’historique récent de la conversation (10 derniers messages) de manière temporaire (24 h), effacé à la clôture ou expiration. 
2.18 AuditEvent
Journal d’audit sans données personnelles.
Champs : tenant, utilisateur, action, entité, ancienne valeur, nouvelle valeur.
2.19 Configuration
Paramètres métier du tenant : messages, ton, horaires, notifications, confidentialité.
3. Relations clés
Tenant → toutes les entités.
Product → Category.
Product → Variants et OptionDefinitions.
Cart → Customer, CartItems → Product/Variant.
Order → Customer, TimeSlot, DeliveryZone.
Conversation → Customer, MessageMetadata, AIState, HumanHandoff.
4. Contraintes et intégrité
Un produit appartient à une catégorie au maximum.
Une variante appartient à un produit, unicité nom par produit.
Un client est unique par tenant et hash Signal.
Un créneau est unique par tenant, début, fin.
Les suppressions respectent des politiques de conservation : suppression conversationnelle ≠ suppression comptable.
5. Indexation
Index sur tenant_id pour toutes les tables.
Index sur statuts de commande, créneaux futurs, produits actifs.
Index sur hash Signal pour retrouver un client.
Index sur customer_id pour conversations et commandes.
6. Migrations
Toute modification de structure passe par migration versionnée.
Aucun changement manuel en production.
Chaque migration est testée sur environnement de test.
Rollback possible.
7. Cas limites
Deux clients réservent la dernière place → verrou transactionnel.
Suppression d’un produit en panier → retirer du panier avec message.
Créneau complet pendant la conversation → recalcul et alternatives.
Modification de prix pendant la conversation → recalcul systématique.
Perte Redis → aucune perte de données critiques.
