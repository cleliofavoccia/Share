# Sommaire
[Qu'est-ce que Share ?](#qu'est-ce-que-share)

[Le système Share](#le-système-share)
- [Ajout d'un produit](#ajout-d'un-produit)
- [Obtenir des points](#obtenir-des-points)
  - [Particularité](#particularité)

[Stack technique](#stack-technique)

[Installation](#installation)
- [Git](#git)

[Lancer l'application](#lancer-l'application)
- [En local](#en-local)
- [Conformité du code](#conformité-du-code)

# Qu'est-ce que Share ?

SHARE est un projet qui se veut social et écologique permettant à chacun de s’émanciper davantage matériellement
        grâce au partage et à l’emprunt de biens matériels en communauté. L’idée est de permettre aux utilisateurs de
        recycler des objets peu utilisés en les prêtant, et de profiter d’objets délaissés par leur propriétaire qui
        peuvent être très utiles selon les besoins de chacun. Aussi, pour consommer mieux et plus que peut le permettre
        son pouvoir d’achat, SHARE veut favoriser l’achat groupé pour des objets conséquents qu’on peut très bien
        partager en famille, entre amis, entre collègues ou entre voisins. La particularité de ce projet est de
        construire un système qui vise à réguler, démocratiser et rendre le plus égalitaire possible le processus de partage.

# Le système Share

Le système Share consiste à louer un produit à sa communauté avec un système de points qui permet de réguler
le droit que l'on a sur un objet, la durée de son utilisation et d'encourager les utilisateurs de la communauté 
à apporter davantage d'objets à l'emprunt pour avoir accès à des objets de plus en plus intéressants.
Les points ne sont pas attribués au mérite de celui qui apportera le plus d’objets à la communauté, mais
simplement à l’importance que la communauté revêt pour ses membres. C’est le nombre d’objets partagés en
communauté qui est récompensé.

## Ajout d'un produit
Le système Share permet à chaque utilisateur d'une communauté à mettre un bien en location au sein
d'une communauté. Lorsqu'un bien est soumis à la communauté, chaque membre doit lui donner une
valeur en point - la valeur du point représente le nombre maximal de jours que l'on peut emprunter
cet objet et le nombre de point qu'un utilisateur doit accumuler pour pouvoir emprunter cet objet.
Une fois que tout le monde lui a donné une valeur, le produit prend la valeur moyenne des votes
utilisateurs comme coût en point.

## Obtenir des points
Les utilisateurs d'une communauté obtiennent les points en fonction des coûts des
objets mis en location. Ils obtiennent le nombre de points totaux des objets mis en location
divisé par le nombre d'utilisateur.
```
Exemple :
Il y a trois utilisateurs dans la communauté GAMERS.

Il y a une PS5 et une NITENDO64. 
La PS5 a été évaluée par les trois utilisateurs à 20 points
La NITENDO64 a été évaluée par les trois utilisateurs à 4 points

Le total des objets en location est de 24 points.

Chaque utilisateur reçoit 8 points.
```

### Particularité

Avec le système Share, le produit
le plus cher est inaccessible à chaque utilsateur qui fait parti de la communauté,
à cause de la règle de répartition des points. Pourquoi ? 

Cela encourage la collectivité
à davantage partager des biens intéressants pour sa communauté pour
individuellement profiter d'objets plus intéressants, tout en faisant profiter la
collectivité par effet.

Pour obtenir le produit le plus cher, il faut que 
la communauté possède en points l'équivalent de ```x``` exemplaires
du produit le plus cher avec ```x = le nombre d'utilisateurs.```

```
Exemple :
Il y a trois utilisateurs dans la communauté GAMERS.

Il y a une PS5 et une NITENDO64. 
La PS5 a été évaluée par les trois utilisateurs à 20 points
La NITENDO64 a été évaluée par les trois utilisateurs à 4 points

Le total des objets en location est de 24 points.

Chaque utilisateur reçoit 8 points.

Pour obtenir la PS5, il faut :

 - Avoir 10 NINTENDO64
    Il y a une PS5 et dix NITENDO64. 
    La PS5 a été évaluée par les trois utilisateurs à 20 points
    Les dix NITENDO64 ont été évaluées par les trois utilisateurs à 4 points

    Le total des objets en location est de 60 points.

    Chaque utilisateur reçoit 20 points. Chaque utilisateur peut acheter la PS5.
    
 - Avoir 3 PS5
    Il y a trois PS5 et une NITENDO64. 
    Les PS5 ont été évaluées par les trois utilisateurs à 20 points
    La NITENDO64 a été évaluée par les trois utilisateurs à 4 points

    Le total des objets en location est de 60 points.

    Chaque utilisateur reçoit 20 points. Chaque utilisateur peut acheter la PS5.
```

## Récupérer des points
Lorsque le produit est emprunté, pour chaque jour qu'on le possède, on récupère un point par jour.
Lorsqu'on rend l'objet à la communauté, on récupère tous ses points. Il est possible de rendre l’objet
quand on veut durant la location.

# Stack technique
- **Base de données** : PostgreSQL et ORM Django
- **Administrateur d’application** : Django avec le pattern design MVT (Modèle, Vue, Templates)
- **Interface graphique** : Bootstrap
- **Environnement virtuel** : Pipenv
- **Logiciel de gestion des versions** : Git
- **Service web d’hébergement de gestion des versions** : GitHub
- **Serveur d’application** : Gunicorn
- **Serveur web** : Nginx
- **Système de monitoring** : Supervisord
- **Tâches CRON** : Cronitor
- **Système de logs** : Sentry

# Installation

## Git
Utiliser la commande git suivante : ```git clone https://github.com/cleliofavoccia/Share.git```


# Lancer l'application

## En local
Activer un environnement virtuel et charger les variables d'environnements.

Lancer la commande suivante pour lancer l'application : ```python manage.py runserver```

## Conformité du code
Lancer flake8 pour vérifier la conformité du code avec la commande suivante : ```flake8 --exclude=./*/migrations/,settings/ --format=html --htmldir=flake-report```.

Pour consulter les résultats de la vérification : Aller dans le dossier ```flake-report``` nouvellement crée -> Ouvrir ```index.html```
