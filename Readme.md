# What is Pur Beurre Substitute?

The aim of this application is to propose a substitute for a food product.
The application use the open database provide by the [Open Food Facts](https://world.openfoodfacts.org/).
This application is made for the project 5 from [OpenClassrooms'](https://openclassrooms.com/fr/projects/157/assignment) Python course.

# How to insall?

Be sure MySQL was installed and works.

Create a user with all privileges:
```SQL
CREATE USER 'pbs'@'host' IDENTIFIED BY 'pbs' -- Replace 'host' by the host name on your server
GRANT ALL ON *.* TO 'pbs'@'host';            -- Don't forget to replace 'host'
```

With your console go to the directory which contains Pur Beurre Substitute.
Then run the following command in your console:
```
mysql -u pbs -p pbs < init.sql
```
This command will create a database named 'PBS' with all associated tables.


# How to use?

The first version of this application is built for being used in a terminal's interface.
The user interacted with it only with his keyboard.

**Important**: for the moment the program is only available in French.

## Home page

On start, the user has two choices:

1. Find a substitute for a food product
2. Find substitute in favorite

The terminal ask the user

```
1. Quel aliment souhaitez-vous remplacer ?
2. Retrouver mes aliments substitués.

Que souhaitez-vous faire ?
```

The user answers with the associated number.
If the user gives a wrong answer (```3``` for example), the program asks the question again.

## Selecting the category

If the user types ```1``` on the home page, the system displays available foods' categories.
Categories are displayed in a list format. Each category is associated with a number.

For example:

```
1. Aliments d'origine végétale
2. Produits laitiers
3. Etc.

Quel catégorie souhaitez-vous consulter ?
```

The user answers with the associated number.
If the user gives a wrong answer (```A``` for example), the program asks the question again.

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
If the user gives a wrong answer (```A``` for example), the program asks the question again.

## Product substitute

When a product is selected by the user, the program displays a substitute.
The user is  informed if there is not a better product. Otherwise, the program displays the product's sheet.

A product sheet contains the following informations:
- Product name
- Description
- Where to buy it (if available)
- Nova score
- Nutriscore
- Link to the Open Food Fact page

The program asks the user if he wants to save this substitute as a favorite:

```
Souhaitez-vous enregistrer ce substitut ? [Oui/Non]
```

If the user save the substitute the system keep the product's sheet as a favorite in the local database.

In any case the user is redirect to the home page.

## Substituted food

If the user type ```2``` on the home page, the program displays each substitutes already selected by the user.
Each product is associated with a number and displayed in a list format.
And the program asks the user:

```
Quel produit souhaitez-vous consulter ?
```

The user answers with the associated number.
If the user gives a wrong answer (```A``` for example), the program asks the question again.

# To do list

See [Trello](https://trello.com/b/W31VG22I/pur-beurre)

# How it works?

## First start

### Download and filter the data

Th application analyze the database to know if its empty or not. If its empty, the application download the data.
All data is downloaded from the [Open Food Fact API](https://fr.openfoodfacts.org/) as JSON files in a ```tmp/``` directory.
Then the application fill the database with those JSON files. Each products are analysed with this method:
- Is there a ```product_name```?
- Is there a ```code```?
- Is there a ```nutriscore_grade```?
- Is there a ```nova_group```?
- And is there an `url`?

We also check the value for ```categories_lc``` is ```fr```.

### Insert data in the database

If all these criteria are satisfied, the product is registered in the database.
If a product is duplicated, for example ```Nutella``` in differrent quantity (big, medium and little pot) or with the same barcode, the application may update the database with the most recently updated product.
