# Suivi du projet

[← Retour à l'accueil](./README.md)

**Dernière mise à jour : 13 octobre 2026.**

## En bref

Le lab fonctionne : les deux machines Windows appartiennent au même domaine,
et Wazuh reçoit leurs événements. Les réseaux du lab sont isolés.
La prochaine étape est de commencer le test d'intrusion dans cet environnement.

Période prévue : **12–16 octobre 2026**. Budget prévisionnel : **20 h au total,
environ 4 h/jour**. Le temps de travail réel n'a pas encore été consigné ;
les attentes de téléchargement et d'installation ne constituent pas une mesure
fiable de ce temps.

## Ce qui a été réalisé

### Lundi 12 octobre — préparer le lab

- Préparation des outils et des images Windows.
- Mise en place du réseau et du serveur central du domaine Active Directory.
- Installation du serveur Wazuh et de la collecte sur la première machine.
- Vérification de la remontée d'une connexion réussie et d'un échec volontaire.

### Mardi 13 octobre — terminer et vérifier l'installation

- Mise en service de la seconde machine et rattachement au domaine.
- Installation de son agent Wazuh : les deux machines transmettent des événements.
- Vérification de la communication entre les deux machines et des services du lab.
- Isolation des deux réseaux après installation.
- Publication des scripts, des corrections et du bilan de validation sur GitHub.

**Résultat : la préparation est terminée et le lab est prêt pour les tests.**
Les [contrôles détaillés](./docs/validation-lab-2026-10-13.md) ont été réalisés
le 13 octobre vers 09:41, heure de Zurich.

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
- [ ] Reconnaître les services et cartographier le domaine.
- [ ] Réaliser les tests d'intrusion et conserver les preuves.
- [ ] Relier chaque technique aux traces ou alertes Wazuh, et documenter les absences de détection.
- [ ] Vérifier la reconstruction complète du lab depuis zéro.
- [ ] Rédiger le rapport et le guide de détection.
- [ ] Compléter les rapports d'avancement et le bilan final.
- [ ] Publier les livrables sur le portfolio.

## Points à surveiller

La préparation, prévue le 12 octobre, s'est terminée le 13. Les tests et la
rédaction restent à réaliser avant le 16 octobre : il faudra prioriser les
techniques documentées pour respecter le budget prévu.

La collecte d'événements est vérifiée. La détection des attaques reste à tester :
une alerte observée pendant l'installation ne prouve pas une attaque réussie.
Le redéploiement complet depuis zéro reste également à vérifier.
