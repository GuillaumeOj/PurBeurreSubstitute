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

- Python + SQL + Utilisation API
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

- Affichage des produits sauvegardé avec le produit d'origine
- Choisir un produit
- Affichage de la fiche produit

## Algorithme pour choisir un substitut

- Compter pour chaque produit le nombre de catégories en commun
- Classer du plus grand au plus petit
- Conserver les produits avec un nutriscore meilleur ou égale
- Classer du meilleur nutriscore au moins bon
- Choisir uniquement `X` produit (**10** par défaut)
