07_CATALOG.md

1. Structure
text
Catalogue
├── Catégorie
│   ├── Produit
│   │   ├── Variante
│   │   ├── Prix
│   │   ├── Stock
│   │   └── Options
2. Catégories
Champs : nom, description, image facultative, position, active/inactive.
Comportement :
Création, modification, désactivation.
Une catégorie désactivée n’apparaît plus.
Les produits d’une catégorie désactivée restent en base mais ne sont pas proposés.
3. Produits
Champs :
Identifiant UUID.
Nom.
Description.
Image facultative.
Catégorie.
Prix de base en centimes.
Unité.
Mode de stock : illimité, limité, indisponible.
Seuil d’alerte.
Statut actif/inactif.
Ordre d’affichage.
Disponibilité : dates de début/fin éventuelles.
Règles :
Aucun produit codé en dur.
Un produit désactivé n’apparaît pas dans les outils catalog.
Si un produit est supprimé alors qu’il est en panier, il est retiré avec message au client.
Modification du catalogue pendant une conversation : les données sont relues à chaque appel.
Les images des produits et catégories sont stockées localement dans un volume Docker (pas de S3 pour le MVP). Le professionnel peut uploader une image via le dashboard. 
4. Variantes
Champs :
Nom.
Description.
Supplément : prix additionnel ou prix fixe.
Stock propre.
Référence.
Image.
Disponibilité.
Règles :
Un produit peut avoir zéro, une ou plusieurs variantes.
Les variantes dynamiques sont retournées par le moteur.
Une variante désactivée ou épuisée n’est pas proposée.
Le client peut choisir une variante ou aucune si le produit n’en a pas.
5. Options
Types :
Choix unique.
Choix multiple.
Texte.
Nombre.
Oui/non.
Règles :
Option obligatoire ou facultative.
Une option obligatoire non remplie bloque la validation.
Les options sont propres à un produit.
Les choix possibles sont stockés de manière structurée.
6. Tarification associée
Le prix affiché provient du moteur de tarification.
Prix produit + suppléments variantes + options + quantité + livraison - remises éventuelles.
Aucun prix dans l’IA ni dans les messages.
7. Permissions
OWNER, ADMIN, MANAGER peuvent gérer le catalogue.
STAFF peut consulter mais pas modifier les prix/suppressions.
8. Tests
Ajout, modification, désactivation, suppression, duplication, réorganisation.
Produit avec variantes, sans variantes.
Options obligatoires.
Variante épuisée.
Produit hors disponibilité.
Modification pendant conversation.
