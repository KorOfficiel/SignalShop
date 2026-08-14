12_HUMAN_HANDOFF.md
1. États
État
Signification
AI_ACTIVE
IA active
HUMAN_WAITING
Demande humaine en attente
HUMAN_ACTIVE
Humain actif, IA en pause
AI_RESUMING
Reprise automatique après expiration

2. Règles absolues
Lorsqu’un humain envoie un message dans une conversation, l’IA passe en pause.
Pendant HUMAN_ACTIVE, l’IA reste silencieuse.
L’humain est prioritaire sur l’IA.
3. Demande humaine
Le client peut demander un humain.
Le système passe en HUMAN_WAITING.
Le professionnel est notifié.
Un timer de 15 minutes démarre.
4. Prise en main humaine
Le professionnel prend la main depuis le dashboard. L’état passe à HUMAN_ACTIVE. Le timer est annulé.
Pour le MVP, la prise en main humaine se fait uniquement via le dashboard. Le numéro Signal professionnel sert uniquement aux notifications. L’intervention via Signal (envoi d’un message depuis le numéro whitelisté) est prévue comme évolution future avec un protocole dédié. 
5. Expiration du timer
Si aucune réponse humaine avant 15 minutes :
HUMAN_WAITING → AI_RESUMING.
Le client peut être prévenu que l’assistant reprend.
Puis AI_ACTIVE.
6. Reprise manuelle
Le professionnel peut cliquer « Reprendre avec l’IA ».
L’état revient à AI_ACTIVE.
7. Stop IA
Le professionnel peut arrêter l’IA globalement ou par conversation.
Arrêt temporaire ou permanent jusqu’à réactivation.
Pendant l’arrêt, les messages clients sont traités par l’humain ou mis en attente.
8. Identification du professionnel
Le numéro Signal professionnel est whitelisté pour l’envoi de notifications uniquement. Aucune intervention via Signal n’est possible pour le MVP.
Authentification dashboard requise pour les actions manuelles. 
9. Cas limites
Timer expire au moment où l’humain répond → priorité à l’humain.
Client renvoie un message pendant HUMAN_ACTIVE → IA silencieuse.
Reprise automatique alors qu’un humain est en train d’écrire → éviter avec statut de frappe ou délai.
10. Tests
Humain répond avant timer.
Humain ne répond pas, timer expire.
Timer annulé.
IA reprend automatiquement.
Reprise manuelle.
Stop IA manuel.
Intervention via Signal (test futur, non MVP) 
