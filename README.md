# Qu'est-ce que Share ?

Mettre en commun des biens pour davantage d'émancipation matérielle avec
un système de gestion d'emprunt qui donne un intérêt à la fois individuel et collectif de
partager avec sa famille, ses amis ou encore ses voisins !

# Le système Share

Le système Share consiste à louer un produit à sa communauté avec un système de points
qui permet de réguler le droit que l'on a sur un objet, la durée de son utilisation et 
d'encourager les utilisateurs de la communauté à apporter davantage d'objets à l'emprunt
pour avoir accès à des objets de plus en plus intéressants.

## Un système de points ?

### Ajout d'un produit
Le système Share permet à chaque utilisateur d'une communauté à mettre un bien en location au sein
d'une communauté. Lorsqu'un bien est soumis à la communauté, chaque membre doit lui donner une 
valeur en point - la valeur du point représente le nombre maximal de jour que l'on peut emprunter
cet objet et le nombre de points qu'un utilisateur doit accumuler pour pouvoir emprunter cet objet. 
Une fois que tout le monde lui a donné une valeur, le produit prend la valeur moyenne des votes 
utilisateurs comme coût en point.

### Comment avoir des points pour emprunter les objets proposés par la communauté ?
Les utilisateurs d'une communauté obtiennent les points en fonction des coûts des 
objets mis en location. Ils obtiennent le nombre de points totaux des objets mis en location
divisé par le nombre d'utilisateur. 
```
Exemple :
Il y a trois utilisateurs dans la communauté GAMERS.

Il y a une PS5 et une NITENDO64. 
La PS5 a été évalué par les trois utilisateurs à 20 points
La NITENDO64 a été évalué par les trois utilisateurs à 4 points

Le total des objets en location est de 24 points.

Chaque utilisateur reçoit 8 points.
```

### Comment puis-je obtenir la PS5 ?

Avec le système Share, le produit 
le plus cher est inaccessible à chaque utilsateur qui fait parti de la communauté, 
à cause de la règle de répartition des points. Pourquoi ? 

Cela encourage la collectivité 
à davantage partager des biens intéressants pour sa communauté pour 
individuellement profiter d'objets plus intéressants, tout en faisant profiter la 
collectivité par effet.

#### Règle d'or
Pour obtenir le produit le plus cher, il faut que la communauté
possède en points l'équivalent de x exemplaire du produit le plus cher
avec x = le nombre d'utilisateur.

```
Exemple :
Il y a trois utilisateurs dans la communauté GAMERS.

Il y a une PS5 et une NITENDO64. 
La PS5 a été évalué par les trois utilisateurs à 20 points
La NITENDO64 a été évalué par les trois utilisateurs à 4 points

Le total des objets en location est de 24 points.

Chaque utilisateur reçoit 8 points.

Pour obtenir la PS5, il faut :
 - Avoir 10 NINTENDO64
    Il y a une PS5 et dix NITENDO64. 
    La PS5 a été évalué par les trois utilisateurs à 20 points
    Les dix NITENDO64 ont été évalué par les trois utilisateurs à 4 points

    Le total des objets en location est de 60 points.

    Chaque utilisateur reçoit 20 points. Chaque utilsateur peur acheter la PS5.
    
 - Avoir 3 PS5
    Il y a trois PS5 et une NITENDO64. 
    Les PS5 ont été évalué par les trois utilisateurs à 20 points
    La NITENDO64 a été évalué par les trois utilisateurs à 4 points

    Le total des objets en location est de 60 points.

    Chaque utilisateur reçoit 20 points. Chaque utilsateur peur acheter la PS5.
```

### Récupérer ses points pour avoir d'autres objets
Lorsque le produit est emprunté, pour chaque jour qu'on le 
possède, on récupère un point par jour.
Lorsqu'on rend l'objet à la communauté, on récupère tous ses points.

# Installation

## Git
Utiliser la commande git suivante : ```git clone https://github.com/cleliofavoccia/Share.git```


# Lancer l'application

## En local
Activer un environnement virtuel et charger les variables d'environnements.
Lancer la commande suivante pour lancer l'application : ```python manage.py runserver```

## Conformité du code
Lancer flake8 avec la commande suivante : ```flake8 --exclude=./*/migrations/,settings/ --format=html --htmldir=flake-report
```
