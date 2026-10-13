# GOAD Purple Team Lab

Projet personnel de test d'intrusion sur un environnement Active Directory
volontairement vulnérable ([GOAD](https://github.com/Orange-Cyberdefense/GOAD)).
Wazuh sert à observer les traces des tests et à vérifier leur détection.

Ce projet sert aussi de rendu PPE pour le cours *Techniques de gestion de
projets* (CFC 306, Projet 5).

## Où en est le projet ?

**Dernière mise à jour : 13 octobre 2026. Le lab est prêt pour les tests.**

| Étape | Avancement |
| --- | --- |
| Installer le lab et son réseau isolé | Terminé et vérifié |
| Installer Wazuh et recevoir les événements des deux machines | Terminé et vérifié |
| Réaliser le test d'intrusion | À faire — prochaine étape |
| Vérifier la détection de chaque technique d'attaque | À faire |
| Tester la reconstruction complète du lab | À faire |
| Rédiger le rapport et le bilan, puis publier sur le portfolio | À faire |

Les événements reçus jusqu'ici proviennent de la préparation et des contrôles.
Aucune compromission du domaine n'est encore revendiquée.

**[Lire le suivi du projet : réalisations, difficultés et prochaines étapes](./SUIVI.md)**

## Planning

Du **12 au 16 octobre 2026**, avec un budget prévisionnel d'environ
**20 heures au total, soit 4 heures par jour**.
La préparation a débordé sur le 13 octobre ; le temps de travail réel reste à consigner.

## Documents

- [Cahier des charges](./cahier-des-charges.md) : objectifs, périmètre, planning et gestion du projet.
- [Scénario de test](./kvm/SCENARIO.md) : tests prévus et détections à vérifier.
- [Validation du lab](./docs/validation-lab-2026-10-13.md) : contrôles réalisés le 13 octobre.
- [Installation et commandes](./kvm/README.md) : utilisation technique du lab.
- [Journal technique](./docs/journal-demarrage.md) : détail des problèmes et des corrections.

## Environnement retenu

MINILAB adapté à KVM/libvirt : un contrôleur de domaine et un serveur membre,
tous deux sous Windows Server 2019. Les outils d'attaque sont sur l'hôte.
Wazuh reçoit les événements des deux machines, sans tableau de bord ni indexeur.
Les deux réseaux du lab sont isolés.
