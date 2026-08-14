11_DELIVERY.md

1. Livraison
Le professionnel livre lui-même dans un rayon défini.
La livraison est configurable : activation, zones, tarifs, minimum, gratuité, délais, créneaux.
Une zone peut être non desservie.
2. Zones
Le professionnel définit des zones géographiques.
Exemple : Zone A 5 €, Zone B 8 €, Zone C non disponible.
Les tarifs sont stockés en centimes.
3. Adresses
Le client renseigne une adresse complète.
Instructions de livraison optionnelles.
Validation basique de présence des champs nécessaires.
L’adresse n’est pas exposée inutilement.
Champs obligatoires : rue, ville, code postal. Complément d’adresse optionnel. Instructions de livraison optionnelles. 
4. Confidentialité
Les adresses sont supprimées après livraison.
Tant que la commande n’est pas terminée, l’adresse reste nécessaire.
Les logs ne contiennent jamais l’adresse complète.
L’adresse est supprimée après la livraison de toutes les commandes actives du client, ou 30 jours après la dernière commande, selon la première éventualité. 
5. Cas limites
Adresse incomplète → demander les champs manquants.
Zone non desservie → proposer une alternative ou retrait.
Instructions trop longues → limiter la taille.
Adresse supprimée après livraison selon politique.
6. Tests
Zone disponible, tarif correct.
Zone non desservie.
Adresse incomplète.
Suppression d’adresse après livraison.
Minimum de commande éventuel.
