# What is Pur Beurre Substitute?

The aim of this application is to propose a substitute for a food product.
The application use the open database provide by the [https://world.openfoodfacts.org/](Open Food Facts).
This application was made during the project 5 from [https://openclassrooms.com/fr/projects/157/assignment](OpenClassrooms') Python course.
# User documentation

The first version of this application is built for being used in a terminal's interface.
The user interacted with it only with his keyboard.

**Important** : for the moment the program is only available in french.

## Home page

On start, the user has two choices:

1. Find a substitue for a food product
2. Find substitute in favorite

The terminal ask the user

```
1. Quel aliment souhaitez-vous remplacer ?
2. Retrouver mes aliments substitués.

Que souhaitez-vous faire ?
```

The user answers with the associated number.
If the user gives a wrong answer (```3``` for example), the program ask the question again.

## Selecting the category

If the user types ```1``` on the home's page, the system display available foods' categories.
Categories are displayed in a list format. Each category is associated with a number.

For example:

```
1. Aliments d'origine végétale
2. Produits laitiers
3. Etc.

Quel catégorie souhaitez-vous consulter ?
```

The user answers with the associated number.
If the user gives a wrong answer (```A``` for example), the program ask the question again.

## Selecting the food product

Once a category is selected by the user, the application display all food products from this category.
As for the categories, each product is associated with a number and displayed in a list format.

For example:

```
1. Gaspacho [une certaine marque]
2. Gaspacho [une autre marque]
3. Eau de rose [une certaine marque]
4. Eau de rose [une autre marque]

Pour quel produit souhaitez-vous trouver un substitut ?
```

The user answers with the associated number.
If the user gives a wrong answer (```A``` for example), the program ask the question again.

## Product substitute

When a product is selected by the user, the program display a substitute.
The substitute selection is based on the nutri-score and the nutrients level. The substitute must have a better nutri-score and nutrients level than the original product.
If there's no better product, the user is informed. Otherwise the program display the product's sheet.

A product sheet contains the following informations:
- Product name
- Description
- Where to buy it (if available)
- Nutri-score
- Nutrients level
- Link to the Open Food Fact page

The program asked the user if he wants to save this substitute as a favorite:

```
Souhaitez-vous enregistrer ce substitut ? [Oui/Non]
```

If the user save the substitute the system keep the product's sheet as a favorite in the local database.

In any case the user is redirected to the home page.

## Substituted food

If the user type ```2``` on the home's pasge, the program display each substitutes already selected by the user.
Each product is associated with a number and displayed in a list format.
And the program asked to the user:

```
Quel produit souhaitez-vous consulter ?
```

The user answers with the associated number.
If the user gives a wrong answer (```A``` for example), the program ask the question again.
