08_ORDERS.md
1. États de commande
État
Signification
DRAFT
Panier en cours
PENDING_CONFIRMATION
Récapitulatif envoyé, attente de confirmation client
CONFIRMED
Client confirmé, stock et créneau réservés
ACCEPTED
Professionnel a accepté
IN_PREPARATION
En préparation
READY
Prêt
OUT_FOR_DELIVERY
En cours de livraison
COMPLETED
Terminée
CANCELLED
Annulée
REFUSED
Refusée par le professionnel
EXPIRED
Non confirmée à temps

2. Transitions
Gérées uniquement par le moteur de commandes. Exemples :
DRAFT → PENDING_CONFIRMATION après récapitulatif.
PENDING_CONFIRMATION → CONFIRMED après confirmation explicite.
CONFIRMED → ACCEPTED → IN_PREPARATION → READY → OUT_FOR_DELIVERY → COMPLETED.
Annulation possible selon règles.
3. Confirmation
L’IA ne peut jamais considérer une commande validée sans confirmation explicite.
Le client reçoit un récapitulatif clair : produits, quantités, total, créneau, adresse.
Le client doit explicitement confirmer, modifier ou annuler.
4. Panier
Permet ajout, suppression, modification quantité, variante, options.
Recalcul total à chaque changement.
Durée de vie : 24 h sans activité.
En cas d’expiration, le panier devient inactif.
5. Réservation stock et créneau
La réservation a lieu à la confirmation de commande.
Transaction atomique PostgreSQL.
Si stock ou créneau insuffisant, la commande ne se confirme pas.
Libération en cas d’annulation.
6. Modification et annulation
Le client peut modifier tant que le statut le permet.
Le professionnel peut annuler ou refuser.
Une commande annulée libère stock et créneau.
L’historique des changements est conservé.
7. Notes internes
Une note interne n’est jamais envoyée au client.
Visible uniquement dans le dashboard.
Consignée dans l’historique de commande.
8. Cas limites
Stock insuffisant au moment de la confirmation.
Créneau complet au moment de la confirmation.
Commande expirée.
Client confirme puis change d’avis.
Panne base : ne jamais confirmer sans persistance garantie.
9. Tests
Commande simple, multiple, avec variante, option.
Stock insuffisant.
Créneau complet.
Annulation et modification.
Concurrence sur dernier article/créneau.
Expiration du panier.
