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
- Dépôt officiel : github.com/Orange-Cyberdefense/GOAD ; adaptation libvirt locale dans `kvm/`, hors fournisseurs officiellement pris en charge
- Script Makefile pour automatiser le up/down du lab en une commande (objectif à mesurer : redéploiement automatisé ; le premier déploiement nécessite le téléchargement et la conversion des images)

### Lab GOAD

- Variante retenue au démarrage : MINILAB, un domaine `mini.lab` avec un contrôleur de domaine et un serveur membre Windows ; configurations volontairement vulnérables du scénario officiel
- Machines : DC01 et WS01 (Windows Server 2019, respectivement contrôleur de domaine et serveur membre), avec 2 Go de RAM et 2 vCPU chacun, à ajuster si le provisionnement le nécessite
- Avec 16 Go de RAM au total, compter environ 2 Go par VM Windows et lancer le lab par sous-ensembles plutôt que toutes les machines en même temps

### Machine d'attaque

- Au démarrage : outils de pentest sur l'hôte Pop!_OS, avec Impacket et LDAP dans un environnement Python local au projet
- Une VM Kali reste une évolution possible ; elle est reportée pour conserver la mémoire nécessaire aux deux VM Windows et à Wazuh

### Réseau

- Réseau du domaine libvirt isolé ; réseau NAT séparé uniquement pendant le provisionnement, puis retrait du NAT et du relais DNS extérieur avant les attaques
- Segment du domaine partagé entre les outils sur l'hôte et les deux machines Windows ; réseau de gestion distinct pendant le provisionnement

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

- Wazuh manager 4.14.0 déployé en conteneur Docker, limité à 1 CPU / 1 Go RAM ; collecte et alertes JSON, sans indexeur ni tableau de bord
- Agents Wazuh 4.14.0 prévus sur les deux hôtes Windows pour transmettre directement les événements Security, System et PowerShell ; deux agents actifs et collecte réelle validée le 13 octobre
- Pour chaque technique attaquée : vérifier et documenter l'alerte ou la trace générée côté Wazuh (approche purple team)
- Manager démarré dès la préparation ; limite de 1 Go de RAM pour conserver la collecte pendant le provisionnement et les phases d'attaque

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

**Outils principaux :** BloodHound, Impacket, CrackMapExec, Mimikatz, Rubeus, Nmap, Wazuh (détection), agents Wazuh (collecte native des événements Windows).

## Livrables

- Rapport de pentest professionnel (résumé exécutif, findings classés par criticité CVSS, recommandations de remédiation)
- Playbook de détection : mapping technique d'attaque → alerte/règle Wazuh correspondante
- Dépôt GitHub avec README clair et scripts annexes
- Scripts d'automatisation du déploiement (Ansible/Makefile) publiés avec le rapport
- Write-ups détaillés par vulnérabilité exploitée
- Version publiée / anonymisée sur le portfolio (bilelka.com)

## Planning (1 semaine)

- **Lab GOAD** : lundi 12 octobre
- **Test d'intrusion** : mardi 13 au mercredi 14 octobre
- **Rédaction du rapport** : jeudi 15 octobre
- **Publication** : vendredi 16 octobre

Semaine du lundi 12 au vendredi 16 octobre, à raison de \~4h/jour en parallèle d'autres obligations ; chaque phase s'enchaîne sur la suivante, avec peu de marge entre les étapes.

## Gestion de projet

### Méthode

Mini-Kanban (Backlog / En cours / Fait), suivi via GitHub Projects (ou Trello), pour travailler la gestion de projet en parallèle de la partie technique.

### Budget prévisionnel

| Poste | Estimation |
| --- | --- |
| Temps (lab + attaque + rapport + rapports d'avancement) | \~20h sur 1 semaine (\~4h/jour, lundi-vendredi) |
| Outils et licences | 0 CHF (GOAD, Kali, Wazuh, KVM/QEMU : open-source) |
| Infrastructure | 0 CHF (poste personnel, pas de cloud payant) |
| Certification associée (hors périmètre direct) | eJPT \~200 CHF, non comptée dans ce budget |
| **Total** | **\~20h de travail / 0 CHF de coût direct** |

### Rituels

- Point quotidien de 10 minutes : fait hier, prévu aujourd'hui, blocages
- Bilan à mi-parcours (mercredi 14 octobre) : avancement réel vs planning, ajustement si besoin
- Rétrospective finale : ce qui a bien marché / ce qui serait à améliorer, à inclure dans le rapport

### Suivi des risques

| Risque | Impact | Mitigation |
| --- | --- | --- |
| RAM insuffisante (16 Go) pour lab + Kali + Wazuh en simultané | Ralentissement, VM instables | Lancer le lab par sous-ensembles, limiter le manager Wazuh à 1 Go |
| Retard sur le déploiement GOAD (jour 1) | Moins de temps pour l'attaque | Basculer sur une version GOAD allégée si besoin |
| Alertes Wazuh non déclenchées pour certaines techniques | Partie détection incomplète | Ajuster les règles, ou documenter l'absence de détection comme un finding |
| Rapport pas terminé à temps | Livrable incomplet | Rédiger au fil de l'eau dès le mercredi |
| Budget de \~4h/jour insuffisant face à l'ampleur du scénario | Phases écourtées ou périmètre réduit en cours de semaine | Prioriser la compromission du domaine et la détection ; réduire le nombre de techniques documentées si besoin |

### Backlog

Le suivi daté, les résultats et toutes les captures sont réunis dans le [README principal](./README.md#journal-et-captures-décran).

| Tâche | Jour | Statut |
| --- | --- | --- |
| Outils d'attaque sur l'hôte + réseau libvirt isolé | Lun 12 | Fait |
| Déploiement MINILAB (Vagrant/libvirt + Ansible) | Lun 12 | Terminé et vérifié le 13 octobre |
| Installation Wazuh manager + agents | Lun 12 | Manager et deux agents actifs ; collecte réelle validée |
| Reconnaissance et cartographie BloodHound | Mar 13 | Première reconnaissance réalisée le 14 ; cartographie BloodHound à faire |
| Exploitation et mouvement latéral | Mar 13 - Mer 14 | Mot de passe exposé et connexion SMB vérifiés le 14 ; mouvement latéral à faire |
| Compromission domaine (DCSync) + corrélation Wazuh | Mer 14 | À faire |
| Scripts d'automatisation et Makefile | Lun 12 - Mar 13 | Utilisés pour le premier déploiement ; reconstruction complète à vérifier |
| Rédaction rapport + playbook détection | Jeu 15 | À faire |
| Publication GitHub + portfolio | Ven 16 | Dépôt et suivi publiés ; livrables finaux et portfolio à faire |

## Rapports d'avancement

Gabarit utilisé pour chaque rapport envoyé au comité de pilotage (formateur) ; au moins 2 attendus sur la durée du PPE.

### Rapport d'avancement n°1 — mi-parcours (mercredi 14 octobre)

- **Avancement délai :** préparation terminée le 13 au lieu du 12 ; première reconnaissance et premier test guidé réalisés le 14. Les autres tests et les livrables restent à réaliser avant le 16.
- **Avancement coût :** budget prévisionnel de 20 h / 0 CHF de coût direct. Le temps réel n'est pas encore consigné ; la consommation du budget horaire reste à établir.
- **Avancement qualité :** domaine et isolation vérifiés, deux agents actifs ; mot de passe exposé dans une description LDAP confirmé par une connexion SMB réussie, corrélée à l'événement 4624 / règle Wazuh 100101.
- **Risques actifs :** délai restant court, temps réel non mesuré, couverture des techniques encore partielle, reconstruction complète du lab non vérifiée.
- **Décisions / points d'attention :** prioriser un scénario court avec preuves et traces ; signaler l'utilisation des identifiants initiaux du scénario ; conserver les secrets et journaux bruts hors du dépôt public.

[Compte rendu du mercredi et prochaines étapes](./README.md#mercredi-14-octobre--premiers-tests).

### Rapport d'avancement n°2 — clôture (vendredi 16 octobre)

- **Avancement délai :** à compléter
- **Avancement coût :** à compléter
- **Avancement qualité :** à compléter
- **Risques actifs :** à compléter
- **Décisions / points d'attention :** à compléter

## Gestion de l'aléa imprévu

Le PPE prévoit un aléa injecté par le formateur en cours de semaine. En autonomie, le mécanisme suivant est utilisé pour rester dans l'esprit de l'exercice : tirage au sort d'un aléa parmi la liste ci-dessous, le mercredi de la semaine (14 octobre).

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

À rédiger en fin de semaine (vendredi 16 octobre), une fois le projet clos.

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
