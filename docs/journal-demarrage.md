# Journal de démarrage — GOAD Purple Team Lab

## Cadre

- Semaine du 12 au 16 octobre 2026, budget prévisionnel de 20 h (4 h/jour).
- KVM/libvirt conservé ; MINILAB adapté localement hors fournisseurs GOAD officiels.
- DC01 : contrôleur `dc.mini.lab`, 192.168.56.30 ; WS01 : membre `ws.mini.lab`, 192.168.56.31.
- Deux VM Server 2019 de 2 Gio et 2 vCPU ; outils sur l'hôte pour économiser la mémoire.
- Manager Wazuh 4.14.0 en conteneur, limité à 1 Gio / 1 CPU, sans indexeur ni tableau de bord.

## 12 octobre — préparation

Les dépendances et les images ont été épinglées et vérifiées. Le premier démarrage
Windows a nécessité une normalisation de la box avant le provisionnement WinRM.
Le contrôleur et le domaine `mini.lab` ont été configurés avec le scénario GOAD.
L'agent Wazuh du contrôleur a transmis des événements Windows réels :

| Événement | Règle | Validation |
| --- | --- | --- |
| 4624, ouverture de session réseau | 100101 | Authentification pendant la préparation |
| 4625, échec d'authentification | 100100 | Un échec volontaire avec un compte inexistant |

Ces tests valident la collecte ; ils ne prouvent aucune compromission.
La règle DCSync 100102 reste à tester pendant la phase d'attaque.

## 13 octobre — corrections et reprise

1. La découverte des interfaces de GOAD partageait le nom d'interface du premier
   hôte avec le second (`run_once`). Une correction locale calcule ces faits par hôte.
2. L'évaluation de l'image Windows 10 était expirée et provoquait des arrêts
   automatiques. WS01 a été recréé comme serveur membre à partir de la base Server
   2019 dont l'évaluation était active sur DC01.
3. Les deux clones avaient le même SID, empêchant la jonction. Sysprep a généralisé
   uniquement WS01 via une tâche SYSTEM temporaire. Son réseau privé a été
   restauré après le redémarrage, puis la tâche a été retirée.
4. WS01 a rejoint `mini.lab` ; la configuration du scénario est terminée.
5. Le commit `def9df9` a été publié après autorisation explicite concernant les
   adresses privées du lab et les identifiants génériques publics de démarrage.

## Limites et preuves

Les journaux bruts, images, secrets d'enrôlement Wazuh et résultats contenant des
secrets restent locaux et exclus de Git. Un export utilise une liste explicite de
métadonnées d'alertes, sans messages bruts ni commandes.

La jonction, les deux agents, la collecte réelle, les services et l'isolation
finale sont vérifiés.  Le redéploiement complet automatisé reste un objectif à valider.
Aucune technique d'attaque réussie n'est revendiquée à ce stade.
Les durées d'attente des téléchargements et installations ne sont pas assimilées
à des heures de travail ; le temps humain réel reste à consigner.

Le contrôle final a détecté un cache Netlogon sans contrôleur disponible après
le démarrage simultané des deux VM. La découverte a été relancée sur WS01 ;
la relation d'approbation est ensuite valide. Le démarrage isolé lance désormais
DC01 avant WS01 et une validation explicite contrôle le nom, le domaine, le
service Wazuh et la relation d'approbation.

## Dossier de preuves visuelles

Les [captures classées par jour](./preuves/README.md) ont été ajoutées le 14 octobre.
Les vues des 12 et 13 sont des lectures rétrospectives des traces conservées,
explicitement étiquetées. Les originaux locaux sont figés pour conserver leur provenance.
