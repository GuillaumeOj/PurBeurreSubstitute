---
title: "Développeur d'application Python - Projet 5"
author:
  - 'Etudiant : Guillaume OJARDIAS'
  - 'Mentor : Erwan KERIBIN'
  - 'Mentor évaluateur : Addi AIT-MLOUK'
geometry: "left=1cm,right=1cm,top=1cm,bottom=2cm"
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
- un objet pour matérialisé un produit (*Product*)

En plus de ces objets, le programme est accompagné d'un fichier `init.sql` permettant d'initialiser ou réinitialiser la base de données. De plus le fichier `settings.py` permet de regrouper un certain nombre de constantes utilisées pour paramétrer certains aspect de l'application (nombre de produits affichés à l'écran, paramètres de connexion à la base de données, chemin de dossier temporaire, etc.)

## Déroulement

Concrétement, le programme se déroule de la manière suivante :

- Au lancement vérification de l'état de la base de données.
- Si la base de données est vide, téléchargement des produits depuis l'API d'[Open Food Facts](https://fr.openfoodfacts.org/) et insertion des produits dans la base de données. Puis le programme continue son exécution.
- Lancement d'un cycle de sélection pour l'utilisateur·rice (choix d'une catégorie, d'un produit puis d'un substitut).
- Affichage de la fiche produit détaillée pour le substitut sélectionné.
- Si l'utilisateur·rice le souhaite, elle·il peut enregistrer le subsitut et le produit substitué dans la base de données.

# Méthodologie de projet

Pour la réalisation de ce projet, je me suis basé sur une méthode dite agile articulée autours de *User stories*.
Dans ce cas, cette méthode mettait en évidence un seul utilisateur interagissant avec l'application.

Les *Users stories* peuvent être consultées sur le Trello suivant : https://trello.com/b/W31VG22I/pur-beurre

# Bilan

## MySQL

Les bases de données SQL sont des outils très puissants. Elles ont l'avantage, selon moi, d'avoir un fonctionnement de base très facile à prendre en main. Elles restent cependant des outils très puissants permettant de réaliser des recherches très complexes.

Dans ce projet, l'exemple le plus marquant est la requête permettant de sélectionner une liste de substitut.
En effet dans le fonctionnement du programme, un subsitut est caractérisé par :

- au moins un minimum de catégories en commun (3 dans les paramètres de base)
- un nutriscore meilleur ou égal au produit d'origine

Or, les catégories et le nutriscore ne sont pas stockées dans la même table (respectivement ***Categories*** et ***Products***)

Il a donc fallu construire cette requête étape par étape en se posant les questions suivantes :

- quelles informations je souhaite récupérer
- quelles tables je vais devoir interroger
- quels critères de sélection vais-je devoir utiliser
- comment dois-je organiser les résultats

## Utilisation d'une API

- Documentation pas toujours clair
- Données récupérées a traiter avec des pincettes
- Forte dépendance de la stabilité de l'API

## Gestion de projet

- Plus d'assiduité dans le planning
- Prendre des temps pour analyser le travail fait dans son ensemble

