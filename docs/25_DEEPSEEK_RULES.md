25_DEEPSEEK_RULES.md
1. Règles fondamentales
La documentation maître est la source de vérité.
Ne jamais inventer une exigence métier absente.
Ne jamais supprimer une fonctionnalité existante sans autorisation.
Ne jamais modifier l’architecture fondamentale sans validation.
Ne jamais contourner les règles métier avec l’IA.
Ne jamais stocker inutilement des données personnelles.
Ne jamais mettre de secrets dans le code.
Ne jamais considérer une fonctionnalité terminée sans tests.
2. En cas d’ambiguïté ou contradiction
Arrêter l’implémentation concernée.
Produire un rapport d’ambiguïté ou de contradiction.
Ne pas choisir silencieusement.
3. Développement
Lire la documentation.
Analyser l’architecture.
Ne pas coder avant validation.
Créer les fichiers et les tests.
Exécuter les tests.
Corriger les erreurs.
Documenter les changements.
Ne pas casser les modules existants.
4. Ordre de travail recommandé
Architecture → Database → Core → Signal Adapter → Catalog → Orders → Scheduling → Inventory → Conversation Engine → AI → Human Handoff → Dashboard → Notifications → Security → Tests → Deployment.
5. Validation
Spécification.
Implémentation.
Tests unitaires.
Tests intégration.
Revue sécurité.
Documentation.
Test de non-régression.
6. Livraisons
AMBIGUITY_REPORT en cas de doute.
CHANGELOG à jour.
Documentation technique et client à jour.
