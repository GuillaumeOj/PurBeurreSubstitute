---
title: Projet 5 - Utilisez les données publiques de l'OpenFoodFacts
subtitle: Parcours OpenClassrooms - Développeur d'application Python
author:
  - 'Etudiant : Guillaume OJARDIAS'
  - 'Mentor : Erwan KERIBIN'
  - 'Mentor évaluateur : Addi AIT-MLOUK'
---

# Présentation du projet

## Cahier des charges

- Utilisation des données d'Open Food Facts
- Programme au moins dans un terminal
- Les recherches utilisateurs se font dans une base de données MySQL
- Proposer un substitut à un aliment donné

## Code source

- Python + SQL + Request
- Github -> [Pur Beurre Substitute](https://github.com/GuillaumeOj/PurBeurreSubstitute)
- Arborescence du programme

# Déroulement du programme

## Menu principal

- Choisir un substitut
- Trouver un produit sauvegardé


## Choisir un substitut

- Choisir la catégorie
- Choisir un produit
- Choisir un substitut
- Affichage de la fiche produit
- Choisir de sauvegarder le produit

## Trouver un produit sauvegardé

- Affichage des produits sauvegardés avec le produit d'origine
- Choisir un produit
- Affichage de la fiche produit

## Algorithme pour choisir un substitut

- Compter pour chaque produit le nombre de catégories en commun
- Classer du plus grand au plus petit
- Conserver les produits avec un nutriscore meilleur ou égale
- Classer du meilleur nutriscore au moins bon
- Choisir uniquement ***10*** produit (valeur par défaut)

# Bilan du projet

## MySQL

- Apprentissage rapide sur les bases
- Apprentissage plus difficile sur une utilisation complexe
- Construire ses requêtes complexes étapes par étapes
- Faire le traitement des données au maximum sur la base de données

## API

- En théorie (cours) notions simples
- En pratique plus complexe, car documentation faible
- Toujours expérimenter avant de lancer l'utilisation en production

## Python

- Amélioration notable par rapport au projet 3
- Meilleure utilisation des classes et des méthodes
- Gestion des erreurs à perfectionner
- Grosse avancée, le meilleur reste à venir !

## Fin

Merci pour votre attention