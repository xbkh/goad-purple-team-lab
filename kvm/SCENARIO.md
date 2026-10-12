# Scénario purple team retenu

Périmètre exclusif : MINILAB, DC01 `192.168.56.30`, WS01 `192.168.56.31`, domaine `mini.lab`.
Le réseau NAT de provisionnement doit être retiré avant les tests.

La réalisation du scénario dépend d'un domaine fonctionnel et de deux agents
Wazuh actifs. Vérifier la collecte par un événement bénin avant toute attaque.

| Étape | Test envisagé | Preuve attendue | Détection à vérifier |
| --- | --- | --- | --- |
| Reconnaissance | Ports AD/SMB/WinRM sur les deux IP autorisées | Résultat horodaté | Un scan n'est pas forcément visible dans les journaux Windows collectés |
| Énumération | LDAP : utilisateurs, groupes, descriptions | Attributs pertinents et chemin vers les privilèges | Traces éventuelles ; absence d'alerte à documenter |
| Identifiants faibles | Échec contrôlé puis authentification avec un compte du scénario | Session SMB/LDAP réellement établie | 4625 / 4624, règles 100100 / 100101 |
| Mouvement latéral | Exécuter uniquement `whoami` sur WS01 via WMI avec le compte administrateur local du scénario | Identité retournée, heure et hôte | 4624 / 4688 ; corrélation avec l'exécution WMI |
| Compromission du domaine | Vérifier l'appartenance Domain Admins puis DCSync limité à un compte du lab | Succès réel de la réplication ; secrets conservés uniquement en local | 4662 et droits de réplication, règle 100102 |
| Nettoyage | Vérifier les fichiers temporaires et les services créés par les outils | État après test | Journal des actions |

Les identifiants fournis par le scénario GOAD sont connus lors de la préparation.
Le rapport doit préciser quand un test les utilise : cela valide une technique
guidée, sans prétendre qu'ils ont été découverts lors d'un test à l'aveugle.

Un événement 4624 seul ne prouve pas un mouvement latéral ou un pass-the-hash.
Un événement 4662 doit être corrélé à l'utilisateur, aux GUID de réplication,
à l'hôte source et à l'heure du test ; il peut être légitime entre contrôleurs.
Les règles et étapes ci-dessus sont prévues, pas encore validées sur les VM.
