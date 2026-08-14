01_REQUIREMENTS.md
1. Objectif général
Fournir un assistant commercial conversationnel accessible uniquement via Signal pour les clients, piloté par une IA qui interprète le langage naturel mais ne décide jamais les règles métier. Le professionnel dispose d’un dashboard web responsive pour configurer catalogue, prix, stocks, créneaux, livraison, notifications, confidentialité et intervention humaine.
2. Utilisateurs
2.1 Client final
Utilise Signal uniquement.
Peut consulter le menu, poser des questions, sélectionner produits, variantes, options, quantités.
Peut créer et modifier un panier, choisir un créneau, une adresse, un mode de livraison.
Peut confirmer, modifier, annuler une commande selon les règles.
Peut demander à parler à un humain à tout moment.
Ne voit jamais de messages techniques ni de données d’autres clients.
2.2 Professionnel
Utilise le dashboard web responsive.
Reçoit des notifications dans le dashboard et sur un numéro Signal distinct.
Peut gérer commandes, catalogue, prix, stocks, créneaux, livraison, IA, confidentialité, utilisateurs.
Peut intervenir manuellement dans une conversation.
Ne manipule jamais SQL, Docker, API, JSON, fichiers de configuration techniques.
2.3 Administrateur technique
Facultatif.
Accès réservé à la maintenance serveur, déploiement, surveillance, sauvegardes.
N’a pas automatiquement accès au contenu client sauf nécessité opérationnelle contrôlée.
3. Exigences fonctionnelles principales
Module
Exigence clé
Signal
Canal client exclusif, adapter isolé, gestion deux comptes distincts
Conversation
Menu structuré + langage naturel, états IA/humain
Catalogue
Dynamique, hiérarchie catégorie → produit → variante → options
Tarification
Moteur de tarification unique, aucun prix codé en dur
Panier
Ajout, modification, recalcul, expiration après 24 h d’inactivité
Commandes
États définis, confirmation explicite client, réservation atomique stock/créneau
Créneaux
Capacités, exceptions, alternatives automatiques
Stock
Illimité, limité, indisponible, réservation à la confirmation
Livraison
Rayon défini, zones tarifaires, adresses supprimées après livraison
IA
Orchestration par outils, refus d’invention, résistance à l’injection
Humain
Priorité humaine, pause IA, timer de 15 minutes
Dashboard
Toutes les actions métier sans code, mobile-first
Confidentialité
Minimisation, suppression sélective/totale, politiques de conservation
Notifications
Événements configurables, anti-spam
Sécurité
Authentification, rôles, isolation par tenant/client, logs sans données sensibles

4. Exigences non fonctionnelles
Disponibilité : 24/7 sur serveur Linux VPS unique, redémarrage automatique.
Performance : réponse Signal rapide, dashboard réactif, aucune requête bloquante inutile.
Résilience : pannes Signal, IA, base et queue gérées sans perte incohérente de commande.
Sécurité : secrets hors code, chiffrement au repos des données sensibles, protections brute-force.
Observabilité : health checks, logs techniques sans données personnelles, corrélation des opérations.
Évolutivité : préparation multitenant, modules activables/désactivables.
Qualité : tests unitaires, intégration, concurrence, sécurité, suppression, non-régression.
Accessibilité : contrastes, navigation clavier, textes d’erreur compréhensibles.
Internationalisation : textes séparés du code, français par défaut.
5. Décisions déjà validées
Décision
Valeur retenue
Paiement MVP
À la livraison, en espèces uniquement
Livraison
Le professionnel livre lui-même dans un rayon défini
Comptes Signal
Un numéro service clients + un numéro professionnel distinct
Conservation conversations
30 jours par défaut
Conservation commandes
1 an
Adresses
Supprimées après livraison
Timer handoff
15 minutes
Identification pro
Numéro Signal professionnel whitelisté
Nom provisoire
SignalShop
Ton
Vouvoiement
Fournisseur IA
DeepSeek
Devise
EUR, centimes entiers
Expiration panier
24 h sans activité
Réservation stock
À la confirmation de commande
Fallback IA
Message d’excuse + proposition de parler à un humain

6. Critères de fin de projet
Le projet est terminé lorsque tous les éléments suivants sont opérationnels et testés :
Signal fiable, UX client complète, catalogue dynamique, tarification moteur, panier, commandes avec états, stock atomique, créneaux et capacités, livraison, IA par outils, handoff humain, dashboard complet, notifications, confidentialité/suppression, sécurité, backups testées, monitoring, H24, tests, documentation, déploiement reproductible.
