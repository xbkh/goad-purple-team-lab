# Preuves visuelles par journée

[← Suivi du projet](../../SUIVI.md)

## Captures directes dans les VM

**[Ouvrir les quatre captures des logiciels Windows — 14 octobre](./2026-10-14/captures-directes/README.md)**

Active Directory sur DC01, appartenance de WS01 au domaine, PowerShell et
service Wazuh dans le gestionnaire des services. Chaque image possède une
légende, une date et une limite d’interprétation.

## Archives et résultats conservés par journée

Les six images ci-dessous montrent un lecteur de traces, distinct des captures
directes des VM accessibles ci-dessus.

Les images sont de véritables captures d'un **lecteur local de traces**.
Elles montrent des extraits de résultats conservés, avec leur source et leur
sélection indiquées. Elles ne sont pas des captures originales de terminal ou
d'un tableau de bord Wazuh.

**Pour les 12 et 13 octobre, aucune capture originale n'a été conservée.**
Les images de ces journées ont été réalisées le 14 à partir des traces disponibles.
La date de la journée et celle de la capture sont affichées séparément.

| Journée | Preuves disponibles | Nature |
| --- | --- | --- |
| [Lundi 12 octobre](./2026-10-12/README.md) | Installation de l'agent DC01 et événements Wazuh réels | Lecture rétrospective, capturée le 14 |
| [Mardi 13 octobre](./2026-10-13/README.md) | Installation des deux agents, isolation et services accessibles | Lecture rétrospective, capturée le 14 |
| [Mercredi 14 octobre](./2026-10-14/README.md) | Quatre captures directes des VM ; scan Nmap, connexion de bob et alerte Wazuh, domaine et agents, horloges | Fenêtres Windows et lecture des traces du 14, distinguées dans la galerie |
| Jeudi 15 octobre | À ajouter lors de la séance | Pas de preuve publiée à ce jour |
| Vendredi 16 octobre | À ajouter lors de la séance | Pas de preuve publiée à ce jour |

## Lire et vérifier les preuves

Chaque image est accompagnée d'un extrait texte téléchargeable. Le
[manifeste](./manifest.json) donne les sources locales, la sélection effectuée,
les dates de capture et les empreintes SHA-256 des images, des extraits et des
sources originales. Les originaux sont figés dans les archives locales du lab.
Une empreinte permet de vérifier un fichier ; elle ne certifie pas sa date.
Ces éléments documentent l'exercice local et ne constituent pas une certification externe.

Aucun mot de passe, secret d'enrôlement, clé d'agent ou journal brut complet n'est publié.
La collecte locale et les alertes reçues ne suffisent pas, seules, à prouver toutes
les étapes d'une attaque ; les limites sont indiquées dans les comptes rendus.

## Horodatages du 14 octobre

Avant 06:59 UTC, les horloges Windows avaient environ sept heures d'avance.
Les heures de test enregistrées par l'hôte et les heures de **réception Wazuh**
restent distinctes des heures internes Windows. Le décalage a été contrôlé et
corrigé sur les deux VM, avec moins de deux secondes d'écart lors de la nouvelle
lecture. Les anciens fichiers et leurs heures n'ont pas été réécrits.

## Règle de documentation pour les prochaines séances

1. Avant les tests : vérifier l'heure UTC, le domaine, l'isolation et les agents.
2. Pour chaque étape importante : conserver le résultat et prendre une capture pendant la séance.
3. Dater la capture et l'opération, préciser le compte, la machine et le résultat attendu/observé.
4. Pour la détection : conserver aussi la trace Wazuh corrélée, ou documenter son absence.
5. Vérifier l'absence de secrets avant publication, puis ajouter les images au suivi du jour.

Les résultats de tests guidés doivent rester présentés comme tels. Les erreurs,
les résultats négatifs et les corrections font aussi partie des preuves.
