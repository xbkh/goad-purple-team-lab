# MINILAB sur KVM/libvirt — préparation

Adaptation locale du MINILAB officiel, hors fournisseurs pris en charge par GOAD.
Deux machines prévues : DC01 (192.168.56.30) et WS01 (192.168.56.31).
Allocation initiale : 2 Gio et 2 vCPU par machine, à valider au provisionnement.
La mémoire peut être augmentée avec `GOAD_VM_MEMORY=3072` si nécessaire.

Les images Windows officielles `mayfly` sont épinglées et leurs sommes de contrôle
vérifiées par `scripts/download-box.py`. L'image Windows 10 est publiée avec MD5 :
c'est un contrôle d'intégrité du téléchargement, pas une signature d'authenticité.

Le téléchargement, la conversion VMDK → QCOW2 et l'ajout des boxes libvirt
précèdent le démarrage. Une VM temporaire termine d'abord la configuration
initiale Windows et vérifie WinRM ; son état est ensuite intégré à la box locale.
Cette étape évite de lancer les commandes de provisionnement pendant l'OOBE.
`scripts/vagrant.sh` utilise le conteneur documenté par
vagrant-libvirt, avec le socket libvirt du poste.

Le réseau du domaine est isolé. Un second réseau NAT est prévu uniquement pour
le provisionnement et doit être isolé à son tour avant la phase d'attaque.
Le démarrage de DC01 et WinRM sont validés ; le provisionnement AD est en cours.
Le premier déploiement complet des deux machines reste à valider.
Ne pas lancer les attaques tant que l'isolation complète n'a pas été vérifiée.

## Commandes

Prérequis : Docker, KVM/libvirt opérationnel, Python 3.12 avec venv, qemu-img,
Ruby pour vérifier la syntaxe, et accès utilisateur au socket libvirt.

Depuis `kvm/`, les étapes manuelles sont :

```sh
bash scripts/bootstrap.sh
make download
make boxes
make up
make provision
```

Le manager Wazuh est démarré par `docker compose -f wazuh/compose.yml up -d`
après la création du réseau isolé défini dans `lab-network.xml`.
Son mot de passe d'enrôlement est créé localement par bootstrap et exclu de Git.
Le manager collecte les alertes JSON ; aucun tableau de bord ni indexeur n'est déployé.

L'installation des agents est définie dans `wazuh/install-agents.yml`.
Le suivi local est dans `logs/setup-status.txt` et `logs/finish-setup.log`.
Les journaux et les secrets restent locaux. Les images Windows ne sont pas publiées.

Sources :
- https://vagrant-libvirt.github.io/vagrant-libvirt/installation.html
- https://vagrant-libvirt.github.io/vagrant-libvirt/configuration.html
- https://github.com/Orange-Cyberdefense/GOAD/tree/main/ad/MINILAB
