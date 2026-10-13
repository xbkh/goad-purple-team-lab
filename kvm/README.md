# MINILAB sur KVM/libvirt — préparation

Adaptation locale du MINILAB officiel, hors fournisseurs pris en charge par GOAD.
Deux machines : DC01 (192.168.56.30) et WS01 (192.168.56.31), tous deux sous
Server 2019 ; WS01 remplit le rôle de serveur membre du scénario MINILAB.
Allocation initiale : 2 Gio et 2 vCPU par machine, à valider au provisionnement.
La mémoire peut être augmentée avec `GOAD_VM_MEMORY=3072` si nécessaire.

La box Server 2019 publiée par `mayfly` est épinglée et sa somme SHA-256 est
vérifiée par `scripts/download-box.py`. Les deux VM utilisent la même base,
avec des disques distincts. L'image Windows 10 initialement essayée a une
évaluation expirée qui provoque un arrêt automatique ; elle n'est plus utilisée.

Le téléchargement, la conversion VMDK → QCOW2 et l'ajout des boxes libvirt
précèdent le démarrage. Une VM temporaire termine d'abord la configuration
initiale Windows et vérifie WinRM ; son état est ensuite intégré à la box locale.
Cette étape évite de lancer les commandes de provisionnement pendant l'OOBE.
L'arrêt de cette VM utilise une commande Windows explicite ; la conversion
ne continue qu'après confirmation de son arrêt.
Le provisionnement corrige aussi localement `GOAD/ansible/data.yml` : les
interfaces réseau sont découvertes sur chaque machine, car les noms diffèrent
entre DC01 et WS01. Le chargement partagé de la configuration du lab est conservé.
Avant sa jonction, WS01 est généralisé avec Sysprep si son identité Windows est
identique à celle du contrôleur. Après ce redémarrage, le script restaure son
adresse privée et retire la tâche de préparation temporaire.
`scripts/vagrant.sh` utilise le conteneur documenté par
vagrant-libvirt, avec le socket libvirt du poste.

Le réseau du domaine est isolé. Un second réseau NAT est prévu uniquement pour
le provisionnement et doit être isolé à son tour avant la phase d'attaque.
Les deux VM sont déployées ; le domaine, la relation d’approbation de WS01, les
services et agents Wazuh, la collecte réelle et l’isolation des réseaux sont validés.
Le redéploiement complet depuis zéro reste à valider.
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
`scripts/export-alert-evidence.py` exporte uniquement une liste explicite de
métadonnées d'alertes du lab ; il exclut les messages bruts et les commandes.

Pour reprendre un provisionnement déjà préparé à la jonction au domaine :
`bash scripts/finish-setup.sh --from ad-members.yml`. Cette reprise suppose que
les étapes précédentes de préparation ont réussi.

Sources :
- https://vagrant-libvirt.github.io/vagrant-libvirt/installation.html
- https://vagrant-libvirt.github.io/vagrant-libvirt/configuration.html
- https://github.com/Orange-Cyberdefense/GOAD/tree/main/ad/MINILAB
- https://learn.microsoft.com/en-us/troubleshoot/windows-server/setup-upgrade-and-drivers/windows-installations-disk-duplication
