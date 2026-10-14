# Validation du lab — 13 octobre 2026

Contrôles effectués après isolation, vers 07:41 UTC / 09:41 à Zurich.

| Contrôle | Résultat observé |
| --- | --- |
| DC01 | Nom DC, domaine mini.lab, DNS / Kerberos / LDAP / SMB / WinRM accessibles |
| WS01 | Nom WS, domaine mini.lab, SMB / WinRM accessibles |
| Relation d'approbation WS01 → DC01 | Test-ComputerSecureChannel : True ; nltest : NERR_Success |
| Agents Wazuh | dc (001) et ws (002) actifs ; WazuhSvc démarré sur les deux hôtes |
| Collecte réelle DC01 | Événement 4624 / règle 100101 observé à 07:41:14.582 UTC |
| Collecte réelle WS01 | Événement 4624 / règle 100101 observé à 07:41:15.531 UTC |
| Réseaux goad-purple-lab et goad-purple-mgmt | Aucun élément forward ; relais DNS désactivé |
| Windows | Server 2019 sur les deux VM, évaluations actives lors du contrôle |

Les événements 4624 correspondent aux connexions d'administration de validation.
Un échec contrôlé 4625 / règle 100100 avait également été observé sur DC01 le 12
 octobre. Des alertes 4662 / règle 100102 existent pendant le provisionnement ;
elles ne prouvent pas une attaque DCSync et doivent être corrélées au contexte.

Les preuves détaillées restent locales : health.json, domain-validation.json et
alert-evidence.json dans kvm/logs. Aucun journal brut ni secret n'est publié.

## Reste à réaliser

- Reconnaissance et scénario de pentest documentés.
- Tests de détection corrélés à chaque technique, avec limites et faux positifs.
- Rapport, playbook de détection, bilans et retour d'expérience.
- Validation du redéploiement complet depuis zéro ; aucun délai de 15 minutes
  n'est revendiqué.

## Preuves visuelles

[Capture des traces conservées du 13 octobre](./preuves/2026-10-13/README.md),
réalisée le 14. Aucune capture originale du 13 n’a été conservée.
