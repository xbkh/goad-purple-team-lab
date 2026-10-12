# GOAD Purple Team Lab — Cahier des charges

Projet personnel de pentest interne sur un lab Active Directory volontairement
vulnérable ([GOAD](https://github.com/Orange-Cyberdefense/GOAD)), avec un
volet détection (Wazuh) en parallèle de l'attaque (approche purple team).

Ce projet sert aussi de rendu PPE pour le cours *Techniques de gestion de
projets* (référence CFC 306, Projet 5 — pilotage complet d'un mini-projet de
bout en bout).

Le cahier des charges complet (contexte, périmètre, environnement technique,
méthodologie, planning, gestion de projet, gestion de l'aléa, bilan/REX) est
dans [`cahier-des-charges.md`](./cahier-des-charges.md).

## Démarrage — semaine du 12 au 16 octobre 2026

Budget : environ 20 heures, soit 4 heures par jour.

Le projet démarre avec **MINILAB sur KVM/libvirt** (un contrôleur de domaine et
un poste Windows), adapté localement aux ressources du poste. Les outils de
pentest sont installés dans un environnement Python sur l'hôte pour économiser
la mémoire. Le manager Wazuh fonctionne en conteneur, avec alertes JSON et sans
indexeur ni tableau de bord.

- [Préparation et commandes](./kvm/README.md)
- [Scénario de test](./kvm/SCENARIO.md)
- [Journal de démarrage et limites actuelles](./docs/journal-demarrage.md)

**État au démarrage :** prérequis et manager Wazuh installés ; DC01 démarre avec WinRM et le domaine `mini.lab` est créé ; configuration GOAD
et préparation de WS01 en cours.
La collecte des agents et les détections sur événements réels restent à valider.
Aucun résultat de compromission n'est revendiqué à ce stade.
