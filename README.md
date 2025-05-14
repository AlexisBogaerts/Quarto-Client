# Quarto-Client
**_projet informatique 2025 Bac 2 Quarto_**

__Stratégie__

Il n'y a malheureusement pas beaucoup de stratégie car c'est un bot random. Néanmoins j'estime qu'il peut peut-être faire quelque chose car il va mettre ses pièces de haut en bas et de gauche a droite (l'ordre des cases) et va défiler donc il y a normalement un petit peu plus de chances qu'il gagne contre des bot totalement random.

Comment marche la fonction qui choisis la piece a jouer sans faire de bad move est comme ceci : 

Nous avons une variable pour l'état du plateau, et la pièce qu'on va devoir jouer. J'ai créé un ensemble de toutes le pièces possibles et a chaque fois qu'une pièce est jouée je l'enlève de cet ensemble. On regarde aussi une par une les cases du plateau et dès qu'on voit une case ou il y a None on joue une pièce random de all_pieces à cet endroit la. Si jamais all_pieces n'existe pas ça veut dire qu'il n'y a plus de piece dispo donc on renvoie None et donc on abandonne mais normalement ça ne devrait pas arriver. Avec ceci j'ai fait quelques testes contre moi-même et je n'avais aucun "bad move" donc cela devrait être pareil pendant le tournois à part si un vicieux adversaire arrive a contourner ma magnifique stratégie.

__Bibliothèques__

<ins>socket</ins> : Connexions réseaux

<ins>json</ins> : Conversion en json

<ins>threading</ins> : à servis pour pouvoir écouter en même temps que pouvoir envoyer des pong

<ins>time</ins> : laisser un temps au au serveur de 1 seconde pour préparer le ping car je devais laisse le temps au client de lancer listen()

<ins>random</ins> : simplement pour choisir une pièce aléatoirement

<ins>argv from sys</ins> : Pour récupérer les arguments passés au script Python en ligne de commande, comme le port ou l’adresse IP du serveur.

PS : Je ne sais pas si il faut mettre plus de développement par rapport au code, mais si jamais j'ai mis beaucoup de commentaires dans mon code pour expliquer comment il marche exactement.