# Trivia

## Groupe

Verner Boisson

## Objectif

Appliquer les principes du clean code sur un kata.

## Choix du Kata

J'ai choisi ce kata disponible sur le [github de ChrisHeral](https://github.com/ChrisHeral/trivia) car il avait l'air plus dur et intéressant. Et j'ai choisit de le faire en Python, car c'est le langage que j'ai utilisé le plus dernièrement. Une copie du code legacy se trouve dans le dossier `save/`

## Appréhender

Un premier point en survellant le code.

- Il n'y a pas de test.
- Les méthodes et variables sont mal nommés.
- Il y a du code dupliqué.
- Il est difficile de comprendre ce que fait le programme en une première lecture.
- Il y a beaucoup de nombres et de chaînes de caractère magiques.

## Stratégie

J'ai suivit la stratégie suivante

1. Supprimer les doublons.
2. Renommer les méthodes et les variables.
3. Atomiser les fonctions trop longues.
4. Faire des classes.
5. Déclarer les constantes.
6. Séparer les différentes classes dans des fichiers adapté.
7. Ecrire les test unitaires

## Compréhension du code

Il s'agit d'un "trivial poursuite" simplifié. Le plateau comporte 12 cases. Il y a 4 catégorie de questions et chaque case correspond à une de ces catégorie. Le jeu se joue à partir de 2 joueurs. Les joueurs jouents chacun  leur tour.Le tour d'un joueur se décompose par un lancer de dé, il se déplace sur le plateau de ce résultat ensuite une question correspondant à la case est posée. S'il répond correctement il gagne un point, en revanche s'il se trompe il est en prison et pour en sortir il faut faire un jet de dé dont le résultat est paire. Le jeu se termine lorsqu'un joueur atteint 6 points.

Lorsque j'ai appliqué les pratiques pour avoir un code davantage claire et concis, un comportement a émergé qui n'était pas prit en compte. Lorsqu'un paquet de question est vide. J'ai choisi arbitrairement que le joueur rejoue jusqu'à tomber sur une case où un paquet de question n'est pas vide. Et lorsqu'il n'y a plus aucune question, le jeu se termine et il n'y a aucun gagnant.

## Commandes

Lancer le jeu depuis la racine du projet :

```python trivia.py```

Lancer les test depuis le dossier `test/` :

```python -m nom_du_fichier_de_test.py```
