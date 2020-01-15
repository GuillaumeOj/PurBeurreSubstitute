# Contents page
- [What is Pur Beurre Substitute?](#what-is-pur-beurre-substitute)
- [How to insall?](#how-to-install)
- [How to use this application?](#how-to-use-this-application)
- [How it works?](#how-it-works)

# What is Pur Beurre Substitute?

The aim of this application is to propose a substitute for a food product.
The application use the open database provide by the [Open Food Facts](https://world.openfoodfacts.org/).
This application is made for the project 5 from [OpenClassrooms'](https://openclassrooms.com/fr/projects/157/assignment) Python course.

# How to insall?

Be sure MySQL is installed and works.

Create a user with all privileges:
```SQL
CREATE USER 'pbs'@'host' IDENTIFIED BY 'pbs' -- Replace 'host' by the host name on your server
GRANT ALL ON *.* TO 'pbs'@'host';            -- Don't forget to replace 'host'
```

Clone this current repository on your computer. Run :
```
git clone git@github.com:GuillaumeOj/PurBeurreSubstitute.git
or
git clone https://github.com/GuillaumeOj/PurBeurreSubstitute.git
```

Create a virtual environement in your directory:
```
virtualenv -p python3 env
```
or for PowerShell:
```powershell
virtualenv -p $env:python3 env
```

Activate your virtual environement:
```
source env/bin/activate
```
or for PowerShell:
```powershell
.env/scripts/activate.ps1
```

Install `requirements.txt`:
```
pip install -r requirements.txt
```

Run `main.py` with the argument `--initdb` (or `-i`:
```
python main.py --initdb
```

In the future, you just have to run the previous command without the argument

Enjoy the app !


# How to use this application?

The first version of this application is built for being used in a terminal's interface.
The user interacted with it only with his keyboard.

**Important**: for the moment the program is only available in French.

## Home page

On start, the user has two choices:

1. Find a substitute for a food product
2. Find substitute in favorite

The terminal ask the user

```
=== Que souhaitez-vous faire ===
1. Substituer un aliment
2. Retrouver un aliment déjà substitué
-> Sélectionnez une option (numéro) :
```

The user answers with the associated number.
If the user gives a wrong answer (`3` for example), the application asks the question again.

## Select a category

If the user types `1` on the home page, the system displays available foods' categories.
Categories are displayed in a list format. Each category is associated with a number.

```
=== Choisissez une catégorie ===
1. Aliments d'origine végétale
2. Viandes
3. Boissons
4. Confiseries
5. Produits laitiers
-> Sélectionnez une catégorie (numéro) :
```

The user answers with the associated number.
If the user gives a wrong answer (`A` for example), the program asks the question again.

## Select a product

Once a category is selected by the user, the application display all food products from this category.
As for the categories, each product is associated with a number and displayed in a list format, with the nutrsicore grade and the associated code.

For example:

```
=== Choisissez un produit à subsituer ===
1. Confiture fraises | d | 3250390105220
2. Country Crisp Chocolat Noir (Maxi Format) | d | 5010477348593
3. Trésor  goût chocolat noisette | d | 5053827199568
4. Muesli Crisp Chocolat noir | d | 3250392415099
5. Confiture abricot Bio Maribel | d | 20114701
6. Céréales fourrées chocolat noisette | d | 3250392614959
7. Olives noires dénoyautées | d | 3076820002064
8. Le fleurier | d | 3366321053949
9. Extra Fruits Rouges | e | 5053827204163
10. Muesli Croustillant aux 3 Chocolats | d | 3256220450140
-> Sélectionnez un produit (numéro) :
```

The user answers with the associated number.
If the user gives a wrong answer (`A` for example), the program asks the question again.

## Select a substitute

When a product is selected by the user, the program displays a list of substitute in the same format as for products.
Then the user select the substitute she·he wants to see.

## Display the product's sheet

The information of a product are display like this:
```
Nom commercial : Confiture de fraises // Nom générique : Confiture de Fraises
Catégorie·s : Aliments et boissons à base de végétaux, Aliments d'origine végétale, Petit-déjeuners, etc.
Code barre : 3175681854482
Liste des ingrédients : Fraises (42 %), eau, fibres : dextrine de _blé_, etc.
Quantité : 320 g
Nutriscore : A
Marque·s : Gerblé (NC si pas d'information)
Point·s de vente : Magasins U (NC si pas d'information)
Url Open Food Fact : https://fr.openfoodfacts.org/produit/3175681854482/confiture-etc.
```

The program asks the user if she·he wants to save this substitute as a favorite:
```
=== Souhaitez-vous sauvegarder le produit ? ===
1. Oui
2. Non
-> Sélectionnez une réponse (numéro) :
```

If the user save the substitute the system keep the product's sheet as a favorite in the local database.

In any case the user is redirect to the home page.

## End of the application

The application ask the users if she·he wants to continue to use the application
```
=== Souhaitez-vous continuez à utiliser l'application ? ===
1. Oui
2. Non
-> Sélectionnez une réponse (numéro) :
```

## Substituted food

If the user type ```2``` on the home page, the program displays each substitutes already selected by the user.
Each product is associated with a number and displayed in a list format.

```
=== Quel substitut souhaitez-vous consulter ? ===
1. Trésors ==> Substitué par ==> Crunchy Muesli Chocolat* Noisettes
2. Bacon (15 Tranches) ==> Substitué par ==> Bacon Fumé
3. Nectar d'orange pêche abricot bio ==> Substitué par ==> danao multi vitaminé
4. Bonbons tendres aux fruits ==> Substitué par ==> Stevi Drop
5. Nappage caramel ==> Substitué par ==> Golia Frutta C X 1 Astuccio
6. Camembert Le Rustique ==> Substitué par ==> Fromage blanc Printiligne (0% MG)
-> Sélectionnez le substitut (numéro) :
```

The user answers with the associated number.
If the user gives a wrong answer (`A` for example), the program asks the question again.

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
