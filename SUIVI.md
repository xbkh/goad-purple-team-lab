# Suivi du projet

[← Retour à l'accueil](./README.md)

**Dernière mise à jour : 14 octobre 2026.**

## En bref

Le lab fonctionne : les deux machines Windows appartiennent au même domaine,
et Wazuh reçoit leurs événements. Les réseaux du lab sont isolés.
Les premiers tests ont commencé : services repérés, mot de passe exposé dans
l’annuaire confirmé et connexion avec le compte concerné observée dans Wazuh.

Période prévue : **12–16 octobre 2026**. Budget prévisionnel : **20 h au total,
environ 4 h/jour**. Le temps de travail réel n'a pas encore été consigné ;
les attentes de téléchargement et d'installation ne constituent pas une mesure
fiable de ce temps.

## Captures et preuves

**[Captures directes des VM : Active Directory, PowerShell et service Wazuh](./docs/preuves/2026-10-14/captures-directes/README.md).**
Quatre fenêtres réelles capturées le 14 octobre pendant les vérifications.

[Galerie de toutes les preuves par jour](./docs/preuves/README.md). Pour les
12 et 13, seules les traces conservées et leur lecture rétrospective sont
disponibles ; aucune capture originale des fenêtres n’a été conservée.

## Ce qui a été réalisé

### Lundi 12 octobre — préparer le lab

[Voir la preuve de cette journée](./docs/preuves/2026-10-12/README.md).

- Préparation des outils et des images Windows.
- Mise en place du réseau et du serveur central du domaine Active Directory.
- Installation du serveur Wazuh et de la collecte sur la première machine.
- Vérification de la remontée d'une connexion réussie et d'un échec volontaire.

### Mardi 13 octobre — terminer et vérifier l'installation

[Voir la preuve de cette journée](./docs/preuves/2026-10-13/README.md).

- Mise en service de la seconde machine et rattachement au domaine.
- Installation de son agent Wazuh : les deux machines transmettent des événements.
- Vérification de la communication entre les deux machines et des services du lab.
- Isolation des deux réseaux après installation.
- Publication des scripts, des corrections et du bilan de validation sur GitHub.

**Résultat : la préparation est terminée et le lab est prêt pour les tests.**
Les [contrôles détaillés](./docs/validation-lab-2026-10-13.md) ont été réalisés
le 13 octobre vers 09:41, heure de Zurich.

### Mercredi 14 octobre — reconnaissance et premier constat

[Voir les captures directes et les résultats de cette journée](./docs/preuves/2026-10-14/README.md).

- Lab redémarré et contrôlé : deux machines et deux agents opérationnels.
- Douze ports TCP examinés sur chaque machine.
- Lecture guidée de l'annuaire avec `dave` : mot de passe de `bob` exposé dans sa description.
- Connexion SMB comme `bob` réussie et événement 4624 / règle Wazuh 100101 corrélés.
- Mot de passe et journaux bruts conservés hors du dépôt public.
- Quatre captures directes ajoutées : annuaire Active Directory, contrôleur de domaine, contrôles PowerShell et service Wazuh dans Windows.
- Dossier de preuves visuelles ajouté ; horloges Windows contrôlées et corrigées après détection d’un décalage de sept heures.

[Compte rendu simple de la séance et travail personnel](./docs/seance-2026-10-14.md).
Le mouvement latéral, DCSync et la cartographie complète restent à réaliser.

## Difficultés rencontrées et décisions

| Difficulté | Décision et résultat |
| --- | --- |
| Installation de GOAD à adapter pour KVM | Adaptation locale de MINILAB avec deux machines pour limiter les ressources nécessaires |
| Image Windows 10 expirée, provoquant des arrêts | Remplacement par un serveur membre sous Windows Server 2019 |
| Rattachement au domaine refusé | Correction du choix de l'interface réseau et création d'une identité Windows distincte pour la seconde machine |
| Communication avec le domaine mal initialisée au démarrage | Relance de la découverte du contrôleur ; démarrage désormais prévu avec le contrôleur en premier |

Le détail est dans le [journal technique](./docs/journal-demarrage.md).

## Ce qui reste à faire

- [x] Installer et vérifier le lab.
- [x] Recevoir de vrais événements Wazuh depuis les deux machines.
- [x] Publier le dépôt et le suivi sur GitHub.
- [x] Réaliser une première reconnaissance des services.
- [ ] Compléter la cartographie du domaine.
- [ ] Terminer les tests d'intrusion : première faiblesse vérifiée, suite à réaliser.
- [ ] Relier chaque technique aux traces ou alertes Wazuh, et documenter les absences de détection.
- [ ] Vérifier la reconstruction complète du lab depuis zéro.
- [ ] Rédiger le rapport et le guide de détection.
- [ ] Compléter les rapports d'avancement et le bilan final.
- [ ] Publier les livrables sur le portfolio.

## Points à surveiller

La préparation, prévue le 12 octobre, s'est terminée le 13. Les tests et la
rédaction restent à réaliser avant le 16 octobre : il faudra prioriser les
techniques documentées pour respecter le budget prévu.

La collecte est vérifiée et une connexion SMB de test est corrélée à Wazuh.
Les autres techniques et leurs détections restent à vérifier.
Le redéploiement complet depuis zéro reste également à vérifier.
