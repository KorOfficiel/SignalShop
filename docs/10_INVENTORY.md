10_INVENTORY.md
1. Modes de stock
Mode
Comportement
Illimité
Aucun suivi quantitatif
Limité
Quantité suivie, décrémentée à la confirmation
Temporairement indisponible
Non commandable

2. Gestion du stock
Le stock peut être défini par produit ou par variante.
Seuil d’alerte configurable.
Alerte stock faible dans dashboard et notifications.
Le stock est décrémenté à la confirmation de commande, pas avant.
Libération en cas d’annulation.
3. Concurrence
Les mises à jour de stock sont atomiques.
Interdiction de stock négatif.
Deux clients ne peuvent pas acheter plus que le stock disponible.
Utilisation de transactions avec verrous.
4. Interactions
L’IA appelle check_stock ; le moteur retourne la disponibilité réelle.
Le panier peut dépasser temporairement le stock, mais la confirmation est bloquée.
Le dashboard permet ajustement manuel du stock.
5. Cas limites
Stock insuffisant pendant la confirmation.
Variante épuisée.
Stock mis à jour manuellement pendant la conversation.
Panne base pendant mise à jour du stock : transaction annulée.
6. Tests
Réservation du dernier article.
Stock négatif interdit.
Libération après annulation.
Alerte stock faible.
Stock par variante.
