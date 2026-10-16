# Playbook de détection — GOAD Purple Team Lab

Mapping technique d'attaque → alerte/règle Wazuh correspondante, construit à
partir des tests réalisés sur mini.lab (14–16 octobre 2026). Complète le
[rapport de pentest](./rapport-pentest.md).

---

## 1. Lecture de secrets exposés dans l'annuaire (F1)

| | |
| --- | --- |
| **Technique** | Lecture LDAP de l'attribut `description` d'un compte utilisateur |
| **MITRE ATT&CK** | T1552.001 (Unsecured Credentials: Credentials In Files) |
| **Détection actuelle** | **Aucune.** Une requête LDAP de lecture standard ne génère pas d'événement Windows exploitable par défaut (pas d'audit LDAP activé sur ce lab) |
| **État** | ❌ Angle mort confirmé |
| **Règle proposée** | Activer l'audit LDAP (`Audit Directory Service Access`) côté DC et surveiller les requêtes de recherche à volume anormal depuis un même compte/IP en peu de temps — signal faible mais mieux que rien |
| **Priorité** | Moyenne (la vraie correction est préventive : retirer les secrets des attributs texte, cf. F1 du rapport) |

---

## 2. Authentification avec un identifiant compromis

| | |
| --- | --- |
| **Technique** | Connexion SMB/réseau avec un compte dont le mot de passe a fuité |
| **MITRE ATT&CK** | T1078 (Valid Accounts) |
| **Détection actuelle** | ✅ **Règle 100101** (custom, niveau 6) : Event ID 4624, type de logon 3 (réseau) |
| **Preuve** | 28 événements corrélés le 15 oct. pour `bob` (agent `ws`, source `192.168.56.1`) ; des milliers d'événements cumulés sur les 3 jours de test |
| **Limite connue** | Ne distingue pas un logon légitime d'un logon avec identifiant volé — à corréler manuellement avec le contexte (heure inhabituelle, compte à faible usage habituel, source inattendue) |
| **Règle Wazuh** | `kvm/wazuh/local_rules.xml`, règle `100101` |

---

## 3. Mouvement latéral via partage admin (PsExec/SMBExec)

| | |
| --- | --- |
| **Technique** | Dépôt de binaire via `ADMIN$`, création d'un service Windows démarré en LocalSystem |
| **MITRE ATT&CK** | T1569.002 (System Services: Service Execution), T1021.002 (SMB/Windows Admin Shares) |
| **Détection actuelle** | ✅ **Règle 92650** (native Wazuh, **niveau 12 — critique**) : *"New Windows Service Created to start from windows root path. Suspicious event as the binary may have been dropped using Windows Admin Shares."* |
| **Preuve** | 2/2 tentatives `psexec.py` détectées (`KPGa`/`UspcFEPM.exe`, `mHJz`/`RXGbPfen.exe`), le 15 oct. à 08:26:20Z et 08:26:50Z |
| **Point fort** | C'est la règle la plus sévère déclenchée sur l'ensemble du test, et elle vient du ruleset **par défaut** de Wazuh — aucune règle custom nécessaire pour cette technique précise |
| **Règle Wazuh** | Règle native du ruleset Sysmon/Windows de Wazuh (id 92650) |

---

## 4. Exécution de commande à distance (4688) — écart de détection (F4)

| | |
| --- | --- |
| **Technique** | Création de processus distante via WMI/service (`whoami`, commandes arbitraires) |
| **MITRE ATT&CK** | T1059 (Command and Scripting Interpreter), lié à T1569.002 |
| **Détection actuelle** | ⚠️ **Collecté mais non exploitable.** Event ID 4688 remonté, mais retombe dans la règle générique **67027** (niveau 3 — le plancher), sans corrélation |
| **Preuve** | 729 occurrences du 4688 pendant la seule fenêtre du test du 15 oct., toutes au niveau 3 |
| **Règle proposée (non implémentée)** | ```xml
<rule id="100103" level="8">
  <if_group>windows</if_group>
  <field name="win.system.eventID">^4688$</field>
  <field name="win.eventdata.parentProcessName" type="pcre2">(?i)(services\.exe|wmiprvse\.exe|svchost\.exe)$</field>
  <description>GOAD: creation de processus via un service ou WMI distant</description>
  <mitre><id>T1569.002</id></mitre>
</rule>
``` |
| **Priorité** | **Haute** — c'est le principal écart de détection identifié par ce test |

---

## 5. DCSync — abus des droits de réplication AD

| | |
| --- | --- |
| **Technique** | Simulation d'un contrôleur de domaine pour répliquer les secrets d'authentification (`DS-Replication-Get-Changes[-All]`) |
| **MITRE ATT&CK** | T1003.006 (OS Credential Dumping: DCSync) |
| **Détection actuelle** | ✅ **Règle 100102** (custom, niveau 10) : Event ID 4662 avec les GUID `1131f6aa` (Get-Changes) / `1131f6ad` (Get-Changes-All) dans les propriétés de l'événement |
| **Preuve** | 17 alertes le 15 oct. ; corrélation exacte compte (`alice`), heure (08:30:13.44–.48Z), hôte source et GUID avec le test réel |
| **Limite connue** | Un 4662 seul peut être légitime entre contrôleurs de domaine (réplication normale) — la règle doit être recoupée avec l'identité de la machine source (ici `192.168.56.1`, poste d'attaque, jamais un DC légitime) |
| **Règle Wazuh** | `kvm/wazuh/local_rules.xml`, règle `100102` |

---

## 6. Échecs d'authentification (bruteforce / reconnaissance)

| | |
| --- | --- |
| **Technique** | Tentative de connexion avec un compte invalide ou un mauvais mot de passe |
| **MITRE ATT&CK** | T1110 (Brute Force) |
| **Détection actuelle** | ✅ **Règle 100100** (custom, niveau 5) : Event ID 4625 |
| **Preuve** | 3 alertes sur la durée du test (tests de validation volontaires, compte inexistant) |
| **Règle Wazuh** | `kvm/wazuh/local_rules.xml`, règle `100100` |

---

## Synthèse

| Technique | Détection | Sévérité | Origine de la règle |
| --- | --- | --- | --- |
| Lecture LDAP de secrets | ❌ Angle mort | — | — |
| Authentification avec identifiant volé | ✅ | 6 | Custom (100101) |
| Mouvement latéral (PsExec/SMBExec) | ✅✅ | **12** | **Native Wazuh (92650)** |
| Exécution de commande distante (4688) | ⚠️ Non exploitable | 3 | Native, générique (67027) |
| DCSync | ✅ | 10 | Custom (100102) |
| Échec d'authentification | ✅ | 5 | Custom (100100) |

**Priorité d'amélioration n°1 :** combler l'écart F4 (règle dédiée au 4688
corrélé au contexte de service/WMI distant) — c'est la seule technique du
test sans détection réellement exploitable par un analyste.
