# Fixtures synthétiques

Ces JSON sont des exemples artificiels, pas des événements émis par le lab.
Le moteur `wazuh-logtest` 4.14.0 les décode comme JSON, tandis que les règles
Windows sont rattachées au décodeur interne `windows_eventchannel`.
Les essais JSON seuls n'ont donc pas validé les règles 100100–100102.

Validation restante : observer les événements réels des agents Windows avec
leur identifiant, l'heure, le compte et l'adresse source, puis vérifier les
alertes dans `/var/ossec/logs/alerts/alerts.json`.
Ne pas utiliser ces fixtures comme preuve de détection d'une attaque.
