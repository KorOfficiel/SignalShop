05_CONVERSATION_ENGINE.md
1. Rôle
Le Conversation Engine reçoit les messages Signal, identifie la conversation, applique l’état IA/humain, et route le traitement vers l’IA ou l’humain.
2. Identification du client
Basée sur le numéro Signal hashé.
Aucun compte externe requis.
Un client est créé automatiquement à la première interaction.
Le hash est propre au tenant.
3. États conversationnels
État
Signification
AI_ACTIVE
L’IA répond normalement
HUMAN_WAITING
Demande humaine en attente
HUMAN_ACTIVE
L’humain a pris la main, IA en pause
AI_RESUMING
Reprise automatique après expiration du timer

4. Règles fondamentales
Si l’état est HUMAN_ACTIVE, l’IA ne répond jamais.
Si un humain envoie un message, l’IA passe en pause.
Si l’humain ne répond pas avant 15 minutes, reprise automatique possible.
Le client peut demander un humain à tout moment.
5. Menu structuré
Menu principal configurable par le professionnel.
Les entrées sont numérotées.
Le texte, l’ordre et l’activation sont configurables.
Exemples : voir le menu, commander, poser une question, parler à quelqu’un.
6. Langage naturel
L’IA interprète le langage naturel.
Les intentions et entités sont extraites dans le dialogue.
Toute ambiguïté doit être levée par une question.
Aucune donnée inventée.
7. Traitement d’un message
Le Message Processor vérifie l’idempotence.
Il charge ou crée la conversation.
Il détermine l’état actuel.
Si HUMAN_ACTIVE, le message est transmis au professionnel, l’IA reste silencieuse.
Si AI_ACTIVE, il transmet au AI Orchestrator.
Si demande humaine détectée, il place en HUMAN_WAITING et notifie.
8. Erreurs de compréhension
Message ambigu → demander de reformuler.
Demande hors domaine → réponse polie, pas d’invention.
Message très long ou illisible → proposer une reformulation.
Plusieurs messages rapides → traiter séquentiellement.
9. Cas limites
Client renvoie un message pendant HUMAN_ACTIVE → IA silencieuse.
Timer expire pendant réponse humaine → l’IA ne reprend que si aucun message humain récent.
Client demande « les mêmes que la dernière fois » sans historique conservé → indiquer l’absence d’accès.
Conversation sans activité → expiration selon politique de conservation.
10. Tests
Nouveau client, client existant.
Menu structuré.
Langage naturel simple, ambigu, contradictoire.
Demande humaine.
Reprise IA après timer.
Arrêt IA manuel.
Hors horaires et fermeture exceptionnelle.
