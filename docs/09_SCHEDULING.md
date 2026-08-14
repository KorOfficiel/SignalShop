09_SCHEDULING.md
1. Créneaux
Définis par jour et par horaire.
Exemple : lundi 18h00–18h30, 18h30–19h00.
Capacité par créneau.
Actif/inactif.
2. Disponibilités
Horaires habituels par jour.
Exceptions ponctuelles : fermeture exceptionnelle, vacances, jour férié.
Le professionnel peut fermer aujourd’hui immédiatement.
Le professionnel peut réouvrir.
3. Capacité
Nombre maximal de commandes par créneau.
Quand capacité atteinte : créneau COMPLET.
Le client reçoit automatiquement des alternatives proches.
4. Alternatives automatiques
Si créneau demandé indisponible ou complet, le moteur propose :
Créneaux proches dans la même journée.
Créneaux du jour suivant.
Toujours basés sur les disponibilités réelles.
5. Concurrence
Deux clients ne peuvent pas réserver la dernière place simultanément.
Utilisation de transactions PostgreSQL avec verrou.
Mise à jour atomique du compteur réservé.
6. Fuseau horaire
Stockage interne UTC.
Affichage dans la timezone de l’entreprise.
Conversion correcte pour les messages clients et le dashboard.
7. Erreurs et cas limites
Créneau passé → non proposé.
Modification de créneau pendant une conversation → recalcul.
Fermeture d’un jour → les créneaux de ce jour ne sont plus proposés.
Capacité modifiée à la baisse sous le nombre déjà réservé → bloquer ou prévenir.
8. Tests
Créneau disponible, complet, fermé.
Exception de fermeture.
Alternatives automatiques.
Concurrence sur dernière place.
Timezone.
