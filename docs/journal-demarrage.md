# Démarrage du projet — 12 octobre 2026

Période : 12–16 octobre 2026. Budget : 20 heures, soit 4 heures par jour.

## Vérifications effectuées

- Poste : Pop!_OS 24.04 LTS.
- Mémoire totale observée : environ 14 Gio ; disponible lors du diagnostic : environ 4,2 Gio.
- Stockage disponible : environ 172 Gio.
- KVM présent ; utilisateur membre des groupes kvm et libvirt.
- Libvirt accessible ; réseau `default` actif (NAT, ne constitue pas un réseau isolé).
- VM existante `win10` arrêtée, 2 vCPU et 4 Gio de RAM.
- Ansible, QEMU et virt-manager installés.
- Vagrant et VirtualBox absents.
- Dépôt officiel GOAD téléchargé dans `GOAD/`, révision `992307a`.

## Décisions à prendre

La version téléchargée de GOAD ne propose pas de fournisseur libvirt.
Décision utilisateur : conserver KVM/libvirt. Adaptation locale de MINILAB en préparation.
MINILAB contient un contrôleur de domaine Windows Server 2019 et un poste Windows 10.
Sa configuration VirtualBox réserve 4 000 Mo à chaque VM : la mémoire actuellement
disponible ne suffit pas pour les démarrer ensemble.

L'installation de paquets système nécessite une saisie du mot de passe sudo
par le propriétaire du poste. Aucun mot de passe ne doit être enregistré ici.

## Objectif du premier jour — budget prévisionnel de 4 heures

| Activité | Budget |
| --- | --- |
| Diagnostic, choix de la variante et du fournisseur | 30 min |
| Installation des prérequis et préparation du réseau | 45 min |
| Téléchargement et déploiement du lab | 1 h 45 |
| Vérification du domaine et préparation de la collecte de logs | 45 min |
| Consignation des preuves et des blocages | 15 min |

Ces durées sont des estimations : les téléchargements et le provisionnement
Windows peuvent les dépasser. Consigner le temps réellement passé.

## Prochaines étapes

1. Choisir le fournisseur de virtualisation.
2. Installer les prérequis nécessaires.
3. Libérer suffisamment de RAM pour le lab retenu.
4. Configurer et vérifier un réseau isolé avant toute phase d'attaque.
5. Déployer les machines et valider le domaine.
6. Préparer la collecte Windows/Wazuh avant de tester les techniques.

## État réel

Diagnostic et téléchargement du code terminés. Conteneur Vagrant/libvirt téléchargé.
Images Windows en cours de téléchargement, avec vérification des sommes de contrôle.
Configuration Vagrant préparée dans `kvm/` ; DC01 déployée avec WinRM validé ; WS01 encore en préparation.
L'utilisateur a autorisé la conduite autonome du projet, y compris l'accès libvirt.
Cet accès est fonctionnel et le fichier Vagrant a été validé.
Le réseau `goad-purple-lab` est créé sans transfert vers l'extérieur.
Le manager Wazuh 4.14.0 est démarré, limité à 1 Gio, avec ses ports 1514/1515
publiés uniquement sur l'interface du lab (192.168.56.1).
Ansible 2.18.0, WinRM, Impacket et les collections GOAD sont installés localement.

L'image DC01 est téléchargée et vérifiée en SHA-256 ; sa conversion QCOW2 a passé
`qemu-img check`. L'image WS01 est encore en cours de téléchargement.
Le déploiement des deux VM et le provisionnement du domaine sont enchaînés ;
les journaux locaux dans `kvm/cache/` et `kvm/logs/` permettent de suivre les erreurs.

La collecte des événements réels et les règles Wazuh restent à valider avec les agents.
Les essais JSON synthétiques ne valident pas le décodeur Windows EventChannel.
Le scénario de test est consigné dans `kvm/SCENARIO.md`.
La VM existante `win10` n'a pas été modifiée. Wazuh fonctionne en conteneur ; aucune VM Kali n'a été déployée.

## Sources

- https://orange-cyberdefense.github.io/GOAD/installation/linux/
- https://orange-cyberdefense.github.io/GOAD/labs/MINILAB/
- Configuration inspectée : `GOAD/ad/MINILAB/providers/virtualbox/Vagrantfile`.

## Avancement confirmé le 12 octobre

- DC01 démarre avec Vagrant sur KVM ; WinRM fonctionne sur le réseau du lab.
- Windows confirme son appartenance au domaine `mini.lab` après la promotion.
- Les playbooks GOAD continuent la configuration du contrôleur et du scénario.
- WS01 se télécharge encore ; sa première initialisation Windows sera attendue
  dans une VM temporaire avant l'import dans Vagrant.
- Le manager Wazuh est opérationnel ; les ports 1514 et 1515 sont accessibles
  sur 192.168.56.1. Aucun agent Windows n'est encore confirmé actif.

### Problèmes rencontrés et réponses

- Premier démarrage de l'image convertie : Windows et WinRM n'étaient pas encore
  utilisables. Une copie indépendante a terminé la configuration Windows ;
  SystemSetupInProgress et OOBEInProgress sont à zéro, puis la base a été normalisée.
- Une modification d'un script pendant son exécution a provoqué une erreur de
  lecture ; le script a été relancé depuis sa version finale, sans perte d'image.
- Les réseaux du lab étaient supprimés lors d'un échec Vagrant : leur conservation
  est désormais explicite dans le fournisseur libvirt.
- Un réseau Docker déclaré internal empêchait la publication des ports Wazuh.
  Le manager utilise un réseau Docker standard, avec ports liés uniquement à
  l'adresse du lab. Les réseaux Windows seront isolés après le provisionnement.
- Les copies intermédiaires de conversion ont été retirées après confirmation
  du démarrage pour conserver l'espace disque. Les images originales sont gardées.
