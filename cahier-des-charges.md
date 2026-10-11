# Cahier des charges – Pentest AD (GOAD)

Oct 10, 2026 · @bkh

## Contexte et objectifs

Projet personnel mené en autonomie, conçu comme preuve de compétence concrète en sécurité offensive, exploitable en candidature.

**Objectifs du projet :**

1. Construire un lab Active Directory volontairement vulnérable (GOAD), déployé et redéployable via Infrastructure as Code (Vagrant + Ansible).
2. Mener un test d'intrusion interne complet, de la reconnaissance jusqu'à la compromission totale du domaine, en documentant chaque technique.
3. Mettre en place une supervision Wazuh en parallèle de l'attaque pour capturer et documenter les traces et alertes générées par chaque technique (approche purple team).
4. Produire et publier un rapport de pentest et un playbook de détection de niveau professionnel, utilisables comme pièces de portfolio pour les candidatures en alternance/stage offensive security.

## Alignement avec la grille d'évaluation (cours 306 — Projet 5)

Ce projet sert aussi de rendu PPE pour le cours *Techniques de gestion de projets* (référence CFC 306), sur la base du Projet 5 — Pilotage complet d'un mini-projet de bout en bout.

| Critère | Pondération | Traité dans |
| --- | --- | --- |
| Qualité du plan de projet initial | 20% | Contexte et objectifs, Périmètre, Budget prévisionnel, Planning, Suivi des risques |
| Pilotage effectif (suivi, reporting) | 25% | Gestion de projet (rituels, backlog), Rapports d'avancement |
| Gestion de l'aléa imprévu | 20% | Gestion de l'aléa imprévu |
| Qualité du bilan et du REX | 20% | Bilan de clôture et retour d'expérience |
| Professionnalisme de la communication | 15% | Structure et rédaction de l'ensemble du document |

## Périmètre

**Inclus**

- Déploiement de l'environnement GOAD (plusieurs hôtes Windows formant un ou plusieurs domaines AD), automatisé via Vagrant + Ansible
- Attaques internes Active Directory : énumération, abus de configuration, mouvement latéral, élévation de privilèges jusqu'à la compromission complète du domaine
- Mise en place d'une supervision Wazuh en parallèle, avec capture des alertes et traces générées par chaque technique
- Documentation détaillée de chaque étape (preuves, commandes, captures, alertes correspondantes)

**Exclus**

- Tout système réel ou en production
- Tests externes / surface Internet
- Développement d'un framework C2 personnalisé (hors périmètre)

## Environnement technique

### Poste de travail

Laptop Asus TUF A15 (Ryzen 5 7000 series, 16 Go de RAM, \~200 Go de stockage disponible) sous Pop!\_OS, utilisé comme hôte de virtualisation.

### Hyperviseur et déploiement

- KVM/QEMU via libvirt (interface virt-manager) comme hyperviseur
- Vagrant + plugin vagrant-libvirt + Ansible pour déployer GOAD
- Dépôt : github.com/Orange-Cyberdefense/GOAD (provider libvirt)
- Script Makefile pour automatiser le up/down du lab en une commande (objectif : redéploiement complet en moins de 15 minutes)

### Lab GOAD

- Variante GOAD classique : domaine Windows avec configurations volontairement faibles (ACL, délégation, GPP, etc.)
- Machines : un contrôleur de domaine + plusieurs postes/serveurs membres
- Avec 16 Go de RAM au total, compter environ 2 Go par VM Windows et lancer le lab par sous-ensembles plutôt que toutes les machines en même temps

### Machine d'attaque

- Kali Linux (dernière version stable), en VM
- Allocation : 2 vCPU / 4 Go RAM / 40 Go disque

### Réseau

- Réseau virtuel libvirt isolé (NAT ou réseau interne via virt-manager), sans accès vers l'extérieur
- Un seul segment partagé entre Kali et les machines GOAD

### Boîte à outils par phase

| Phase | Outils |
| --- | --- |
| Reconnaissance | Nmap, enum4linux, ldapsearch |
| Cartographie AD | BloodHound, SharpHound, PowerView |
| Attaques sur identifiants | Impacket (GetUserSPNs, secretsdump), Hashcat |
| Mouvement latéral | CrackMapExec, Evil-WinRM, Impacket (psexec/wmiexec) |
| Post-exploitation / domaine | Mimikatz, Rubeus, DCSync via Impacket secretsdump |
| Rédaction du rapport | Markdown, export PDF (Pandoc ou équivalent) |

### Supervision / détection

- Wazuh manager déployé en VM légère (1 vCPU / 2 Go RAM) à côté du lab GOAD
- Agents Wazuh (ou Sysmon + Winlogbeat) installés sur les hôtes Windows du domaine pour forwarder les logs
- Pour chaque technique attaquée : vérifier et documenter l'alerte ou la trace générée côté Wazuh (approche purple team)
- Lancé uniquement pendant les phases d'attaque pour rester dans le budget de 16 Go de RAM

## Méthodologie

Déroulé type d'un test d'intrusion interne (inspiré du PTES) :

1. Reconnaissance et énumération (ports, services, utilisateurs, partages)
2. Cartographie des chemins d'attaque avec BloodHound
3. Exploitation initiale (Kerberoasting, AS-REP roasting, identifiants faibles)
4. Mouvement latéral (pass-the-hash, pass-the-ticket, WMI/PsExec)
5. Élévation de privilèges et abus de délégation
6. Compromission du domaine (DCSync) et persistance
7. Nettoyage et consignation des preuves
8. Corrélation des alertes et traces générées côté Wazuh pour chaque technique (approche purple team)

**Outils principaux :** BloodHound, Impacket, CrackMapExec, Mimikatz, Rubeus, Nmap, Wazuh (détection), Sysmon + Winlogbeat (forwarding des logs).

## Livrables

- Rapport de pentest professionnel (résumé exécutif, findings classés par criticité CVSS, recommandations de remédiation)
- Playbook de détection : mapping technique d'attaque → alerte/règle Wazuh correspondante
- Dépôt GitHub avec README clair et scripts annexes
- Scripts d'automatisation du déploiement (Ansible/Makefile) publiés avec le rapport
- Write-ups détaillés par vulnérabilité exploitée
- Version publiée / anonymisée sur le portfolio (bilelka.com)

## Planning (3 semaines)

- **Lab GOAD** : 10 au 16 octobre
- **Test d'intrusion** : 17 au 23 octobre
- **Rédaction du rapport** : 24 au 29 octobre
- **Publication** : 30 octobre

Chaque phase démarre le lundi ; la publication clôt la dernière semaine.

## Gestion de projet

### Méthode

Mini-Kanban (Backlog / En cours / Fait), suivi via GitHub Projects (ou Trello), pour travailler la gestion de projet en parallèle de la partie technique.

### Budget prévisionnel

| Poste | Estimation |
| --- | --- |
| Temps (lab + attaque + rapport + rapports d'avancement) | \~60h sur 3 semaines (\~20h/semaine) |
| Outils et licences | 0 CHF (GOAD, Kali, Wazuh, KVM/QEMU : open-source) |
| Infrastructure | 0 CHF (poste personnel, pas de cloud payant) |
| Certification associée (hors périmètre direct) | eJPT \~200 CHF, non comptée dans ce budget |
| **Total** | **\~60h de travail / 0 CHF de coût direct** |

### Rituels

- Point quotidien de 10 minutes : fait hier, prévu aujourd'hui, blocages
- Bilan hebdomadaire : avancement réel vs planning, ajustement si besoin
- Rétrospective finale : ce qui a bien marché / ce qui serait à améliorer, à inclure dans le rapport

### Suivi des risques

| Risque | Impact | Mitigation |
| --- | --- | --- |
| RAM insuffisante (16 Go) pour lab + Kali + Wazuh en simultané | Ralentissement, VM instables | Lancer le lab par sous-ensembles, limiter Wazuh à 2 Go |
| Retard sur le déploiement GOAD (semaine 1) | Moins de temps pour l'attaque | Basculer sur une version GOAD allégée si besoin |
| Alertes Wazuh non déclenchées pour certaines techniques | Partie détection incomplète | Ajuster les règles, ou documenter l'absence de détection comme un finding |
| Rapport pas terminé à temps | Livrable incomplet | Rédiger au fil de l'eau dès la semaine 2 |

### Backlog

| Tâche | Semaine | Statut |
| --- | --- | --- |
| Setup VM Kali + réseau libvirt | S1 | À faire |
| Déploiement GOAD (Vagrant/Ansible) | S1 | À faire |
| Installation Wazuh manager + agents | S1 | À faire |
| Reconnaissance et cartographie BloodHound | S2 | À faire |
| Exploitation et mouvement latéral | S2 | À faire |
| Compromission domaine (DCSync) + corrélation Wazuh | S2 | À faire |
| Script d'automatisation (Makefile) | S2-S3 | À faire |
| Rédaction rapport + playbook détection | S3 | À faire |
| Publication GitHub + portfolio | S3 | À faire |

## Rapports d'avancement

Gabarit utilisé pour chaque rapport envoyé au comité de pilotage (formateur) ; au moins 2 attendus sur la durée du PPE.

### Rapport d'avancement n°1 — fin semaine 1 (16 octobre)

- **Avancement délai :** à compléter
- **Avancement coût :** à compléter
- **Avancement qualité :** à compléter
- **Risques actifs :** à compléter
- **Décisions / points d'attention :** à compléter

### Rapport d'avancement n°2 — fin semaine 2 (23 octobre)

- **Avancement délai :** à compléter
- **Avancement coût :** à compléter
- **Avancement qualité :** à compléter
- **Risques actifs :** à compléter
- **Décisions / points d'attention :** à compléter

## Gestion de l'aléa imprévu

Le PPE prévoit un aléa injecté par le formateur en cours de semaine. En autonomie, le mécanisme suivant est utilisé pour rester dans l'esprit de l'exercice : tirage au sort d'un aléa parmi la liste ci-dessous, le mercredi de la semaine 2 (21 octobre).

**Aléas possibles :**

1. Panne ou corruption d'une VM critique du domaine (DC principal down)
2. La vulnérabilité principale prévue est déjà corrigée dans GOAD, impossible à exploiter comme planifié
3. Les alertes Wazuh restent silencieuses, aucune détection ne remonte
4. Imprévu personnel réduisant le temps disponible de moitié sur 2 jours
5. Panne de ressources (RAM insuffisante pour lancer les VM nécessaires en simultané)

**Gabarit de documentation de la réponse :**

- **Aléa rencontré :** à compléter
- **Impact (délai, coût, périmètre) :** à compléter
- **Décision prise :** à compléter
- **Action corrective :** à compléter
- **Mise à jour du planning :** à compléter

## Bilan de clôture et retour d'expérience (REX)

À rédiger en fin de semaine 3, une fois le projet clos.

- **Résultats obtenus vs objectifs initiaux :** à compléter
- **Respect du délai / budget / qualité :** à compléter
- **Ce qui a bien fonctionné :** à compléter
- **Ce qui serait à améliorer :** à compléter
- **Compétences développées :** à compléter
- **Suite donnée au projet :** à compléter

## Critères de réussite

- Lab GOAD déployé et fonctionnel
- Compromission complète du domaine obtenue (Domain Admin) et documentée
- Alertes Wazuh capturées et documentées pour les principales techniques utilisées
- Lab redéployable en une commande (automatisation validée)
- Rapport rédigé au format professionnel, avec findings notés CVSS
- Rapport, playbook de détection et write-ups publiés sur GitHub et le portfolio
- Au moins une ligne CV/portfolio exploitable en entretien pour appuyer le profil offensive security
