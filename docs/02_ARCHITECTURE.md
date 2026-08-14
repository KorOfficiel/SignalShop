02_ARCHITECTURE.md
1. Principes d’architecture
Séparation des responsabilités : canal Signal isolé derrière un adaptateur, logique métier indépendante, IA en orchestration uniquement.
Source de vérité : base de données PostgreSQL pour prix, stock, créneaux, commandes.
Aucune décision métier dans l’IA : l’IA appelle des outils, le backend applique les règles.
Confidentialité dès la conception : minimisation, conservation courte, logs techniques sans données personnelles.
Modularité : composants remplaçables et testables.
2. Vue logique
text
SIGNAL
   │
   ▼
Signal Adapter
   │
   ▼
Message Bus
   │
   ▼
Conversation Engine
   │
   ├── AI Orchestrator
   └── Human Mode
   │
   ▼
Tool Gateway
   │
   ├── Catalog
   ├── Orders
   ├── Stock
   ├── Schedule
   └── Delivery
   │
   ▼
PostgreSQL
Les composants transverses sont : Redis, système de notifications, système de purge, monitoring, dashboard.
3. Choix techniques cibles
Couche
Choix recommandé
Backend
Python + FastAPI
Base de données
PostgreSQL 16+
Cache/Queue
Redis 7+
Frontend dashboard
React + TypeScript + Vite, framework UI responsive
Reverse proxy
Nginx ou Caddy
Conteneurisation
Docker Compose
Signal
signal-cli via adaptateur dédié
IA
Interface abstraite, fournisseur DeepSeek par défaut

4. Composants et responsabilités
4.1 Signal Adapter
Encapsule signal-cli : JSON-RPC, daemon HTTP, événements SSE.
Reçoit les messages entrants, publie des événements normalisés.
Envoie les messages sortants.
Gère les comptes service et professionnel.
Garantit l’idempotence sur identifiant de message Signal.
4.2 Message Bus
Transporte les événements internes entre l’adapter, le Conversation Engine et les workers.
Assure la mise en file, retries, ordre par conversation si nécessaire.
4.3 Conversation Engine
Identifie la conversation, le client, l’état IA/humain.
Applique les menus structurés et déclenche l’IA en langage naturel.
Empêche l’IA de répondre si un humain est actif.
4.4 AI Orchestrator
Prépare un contexte minimal.
Dialogue avec le fournisseur IA via interface abstraite.
Appelle des outils uniquement à travers la Tool Gateway.
Formate une réponse client non technique.
4.5 Human Mode
Gère les états : AI_ACTIVE, HUMAN_ACTIVE, HUMAN_WAITING, AI_RESUMING.
Gère le timer de handoff.
Gère l’arrêt global ou par conversation de l’IA.
4.6 Tool Gateway
Interface unique entre l’IA et les services métier.
Applique permissions, validation, contextes tenant/client.
Retourne des résultats structurés.
4.7 Services métier
Catalog : catégories, produits, variantes, options.
Orders : panier, commandes, états, transitions.
Inventory : stock, réservations atomiques.
Scheduling : créneaux, disponibilités, capacités, exceptions.
Delivery : zones, tarifs, adresses, instructions.
Notifications : événements et canaux.
4.8 Base de données
PostgreSQL : source de vérité.
Redis : cache court, verrous courts, files, timers.
Aucune donnée critique ne dépend uniquement de Redis.
5. Flux conversationnel type
Un message Signal arrive sur le numéro service.
Le Signal Adapter publie un événement avec identifiant unique.
Le Message Processor identifie conversation, client, état.
Si état IA actif, l’AI Orchestrator reçoit un contexte minimal et génère une réponse ou appelle des outils.
Les outils via Tool Gateway consultent/modifient les services métier en base.
La réponse est envoyée via Signal Adapter.
Si une commande est confirmée, réservation transactionnelle stock/créneau, notification professionnel.
6. Gestion des erreurs transverses
Toute erreur technique côté client donne un message simple et propose un humain.
Les erreurs internes sont journalisées avec code interne, service, heure, gravité.
Aucun traceback, SQL, clé API ou détail technique ne sort vers le client.
7. Règles de modularité
Toute fonctionnalité majeure est activable/désactivable.
Une fonctionnalité désactivée ne doit jamais être appelée.
Les nouveaux modules sont ajoutés sans casser les existants.
Les canaux alternatifs futurs ne remplacent pas Signal.
