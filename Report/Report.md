---
title: "Développeur d'application Python - Projet 5"
author:
  - 'Etudiant : Guillaume OJARDIAS'
  - 'Mentor : Erwan KERIBIN'
  - 'Mentor évaluateur : Addi AIT-MLOUK'
geometry: margin=1.5cm
---

# Présentation

Le but de ce projet était de manipuler une API (Celle d'[Open Food Facts](https://fr.openfoodfacts.org/) en l'occurence) et de stocker l'ensemble des données dans une base de données SQL (ici [MySQL](https://www.mysql.com/fr/)).
L'application du projet permet au final de consulter une base de données de produits alimentaires et de proposer à l'utilisateur·rice un produit alternatif.

## Code source

Url gitHub du projet : https://github.com/GuillaumeOj/PurBeurreSubstitute

# Fonctionnement du programme

## Organisation

Le programme est composé de plusieurs objets :

- l'application avec laquelle l'utilisateur va interagir (*App*)
- un objet dédié aux opérations avec l'API (*API*)
- une classe dédiée aux interactions avec la base de données (*Database*)
- un objet pour la gestion de l'affichage des informations (*Interface*)
- un objet pour matérialiser un produit (*Product*)

En plus de ces objets, le programme est accompagné d'un fichier `init.sql` permettant d'initialiser ou réinitialiser la base de données. De plus, le fichier `settings.py` permet de regrouper un certain nombre de constantes utilisées pour paramétrer certains aspects de l'application (nombre de produits affichés à l'écran, paramètres de connexion à la base de données, chemin de dossier temporaire, etc.)

## Déroulement

Concrètement, le programme se déroule de la manière suivante :

- Au lancement vérification de l'état de la base de données.
- Si la base de données est vide, téléchargement des produits depuis l'API d'[Open Food Facts](https://fr.openfoodfacts.org/) et insertion des produits dans la base de données. Puis le programme continue son exécution.
- Lancement d'un cycle de sélection pour l'utilisateur·rice (choix d'une catégorie, d'un produit puis d'un substitut).
- Affichage de la fiche produit détaillée pour le substitut sélectionné.
- Si l'utilisateur·rice le souhaite, elle·il peut enregistrer le substitut et le produit substitué dans la base de données.

# Méthodologie de projet

Pour la réalisation de ce projet, je me suis basé sur une méthode dite agile articulée autour de *User stories*.
Dans ce cas, cette méthode mettait en évidence un seul utilisateur interagissant avec l'application.

Les *Users stories* peuvent être consultées sur le Trello suivant : https://trello.com/b/W31VG22I/pur-beurre

# Bilan

## MySQL

Les bases de données SQL sont des outils très puissants. Elles ont l'avantage, selon moi, d'avoir un fonctionnement de base très facile à prendre en main. Elles restent cependant des outils très puissants permettant de réaliser des recherches très complexes.

Dans ce projet, l'exemple le plus marquant est la requête permettant de sélectionner une liste de substitut.
En effet dans le fonctionnement du programme, un substitut est caractérisé par :

- au moins un minimum de catégories en commun (3 dans les paramètres de base)
- un nutriscore meilleur ou égal au produit d'origine

Or, les catégories et le nutriscore ne sont pas stockées dans la même table (respectivement ***Categories*** et ***Products***)

Il a donc fallu construire cette requête étape par étape en se posant les questions suivantes :

- quelles informations je souhaite récupérer
- quelles tables je vais devoir interroger
- quels critères de sélection vais-je devoir utiliser
- comment dois-je organiser les résultats

## Utilisation d'une API

L'autre aspect important et nouveau dans ce projet, est l'utilisation d'une API.

La plus grosse difficulté rencontrée aura était dès le début d'être confronté à une documentation peu détaillée sur l'utilisation de celle-ci.
En effet, dans l'idée, les actions possibles avec l'API d'Open Food Facts sont simples (lecture et écriture). La pratique aurait dû être assez proche de ce qui est abordé dans le cours associé au projet ([Utilisez des API REST dans vos projets web](https://openclassrooms.com/fr/courses/3449001-utilisez-des-api-rest-dans-vos-projets-web))

Cependant, toutes les subtilités liées aux arguments à passer lors de la requête ne sont pas expliquées dans le wiki dédié aux développeurs. Par exemple :

- utilisation de `action: process` pour le téléchargement des données
- utilisation de `tagtype_0` puis `tag_contains_0` et enfin `tag_0` pour indiquer que l'on cherche, par exemple, les produis contenant tel terme dans les catégories (cas de l'application)

Finalement, les échanges avec les autres étudiants, les essais multiples et les relectures multiples des informations du wiki, ont rendu possible l'utilisation de l'API.


## Python

De manière plus générale ce projet m'a permis d'approfondir encore l'utilisation de Python.

La notion de programmation orientée objet étant déjà abordée lors du projet 3 (voir : [Aidez MacGyver à s'échapper !](https://github.com/GuillaumeOj/HelpMacGyver)), ce projet aura était l'occasion de continuer dans cette direction et d'approfondir l'utilisation des classes. Notamment, chose nouvelle pour moi, l'utilisation d'une classe *App* plutôt que l'utilisation d'une fonction *main()* (habitude conservée du début de la formation).

L'aspect sur lequel j'aimerais être plus à l'aise est la gestion des erreurs.
Dans ce projet, j'ai essayé de faire appel à l'utilisation de la structure `try... except`. Cependant, je ne suis pas toujours sûr de gérer correctement les exceptions potentiellement levée par cette structure.

# Conclusion

Pour conclure sur ce projet, je dirais qu'il a été riche en nouveauté (MySQL et API REST).

Ce projet m'a poussé à redoubler d'imagination pour trouver des solutions à chaque problème se présentant pour chaque nouvelle fonctionnalité (comment télécharger les produits, comment insérer les produits dans la base de données, comment trouver un substitut, etc.)

Ce projet m'aura surtout permis de comprendre, que même si les cours associés au projet regorge d'informations évidemment utile à la réalisation de celui-ci, toutes les réponses aux questions que l'on se posera durant sa réalisation ne s'y trouve pas.
Il faut sans cesse chercher d'autres sources d'informations, rester à l'affût d'autres méthodes, tester d'éventuels modules plutôt que de réinventer la roue, etc.

En résumé, encore un bon bout de chemin parcouru et encore plein de nouveaux défis à relever pour la suite !
