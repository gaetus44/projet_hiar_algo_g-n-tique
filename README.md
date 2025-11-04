# Projet d'Algorithme Génétique (HIARD)

Ce projet est une implémentation en Python d'un algorithme génétique (AG) simple. L'objectif de l'algorithme est de faire "évoluer" une population d'individus (des chaînes binaires) pour trouver une chaîne binaire cible (la "solution").

L'implémentation est basée sur les concepts présentés dans le cours `Lesson 2 - Genetic Algorithms.pdf`.

## Fonctionnalités principales

Le code actuel implémente un algorithme génétique robuste avec les caractéristiques suivantes :

* **Configuration dynamique** : Au lancement, l'utilisateur peut configurer interactivement les hyperparamètres clés :
    * Taille du tournoi (si applicable)
    * Taux de crossover uniforme (`uniform_rate`)
    * Taux de mutation (Flip, Add, Remove)
    * Activation de l'élitisme
    * Nombre maximum de générations
* **Deux types de sélection** : L'algorithme supporte à la fois la sélection par **tournoi** (`tournament`) et par **roue de la fortune** (`roulette`).
* **Élitisme** : L'option d'élitisme permet de préserver le meilleur individu de chaque génération sans modification, le copiant directement dans la nouvelle population.
* **Génomes de longueur variable** : L'algorithme est conçu pour fonctionner avec des individus dont la longueur du génome (la chaîne binaire) peut varier.

## Implémentation des consignes (PDF p. 25-28)

Ce projet répond à la majorité des objectifs fixés dans les diapositives du cours (à partir de la page 25).

✅ **Ajouter une limite au nombre de générations**
* Implémenté via le paramètre `self.max_gen` dans `simple_genetic_algorithm.py`. L'algorithme s'arrête s'il atteint cette limite.

✅ **Ajouter le support pour la sélection "roulette"**
* Implémenté. L'utilisateur peut choisir `"roulette"` au lancement. La logique de sélection est dans la méthode `roulette_wheel_selection`.

✅ **Support pour les chaînes de bits de longueur variable**
* **Fitness (p. 26)** : La fonction `get_fitness` dans `individual.py` calcule le score en comptant les bits correspondants et en soustrayant une pénalité pour la différence de longueur (`penalty = length_difference * 0.5`).
* **Mutations (p. 27)** : Le code gère plusieurs taux de mutation distincts. La méthode `mutate` applique trois opérations :
    1.  `mutation_rate_flip` (inverser un bit)
    2.  `mutation_rate_add` (ajouter un bit)
    3.  `mutation_rate_remove` (retirer un bit)
* **Crossover (p. 28)** : La méthode `crossover` gère les parents de longueurs différentes. Elle implémente spécifiquement la stratégie qui consiste à "conserver les bits supplémentaires uniquement s'ils appartiennent au parent le plus apte ('fittest parent')".

⚠️ **Support pour un paramètre de "cross-over rate"**
* Partiellement implémenté. Le code possède un `uniform_rate`, qui correspond au "uniform crossover" (la probabilité de prendre un gène du parent 1 plutôt que du parent 2).
* La consigne du PDF pourrait aussi faire référence à un taux de *probabilité de crossover* (la chance que deux parents se reproduisent vs être clonés). Cet aspect n'est pas implémenté ; actuellement, tous les individus non-élites sont générés par crossover.

## Comment l'utiliser

1.  Assurez-vous d'avoir Python 3 installé.
2.  (Optionnel) Modifiez la variable `solution` dans `main.py` pour définir la chaîne binaire cible que vous souhaitez atteindre.
3.  Exécutez le script principal depuis votre terminal :
    ```bash
    python main.py
    ```
4.  Répondez aux questions dans le terminal pour configurer les paramètres de l'algorithme (ou appuyez sur Entrée pour utiliser les valeurs par défaut).
5.  L'algorithme affichera la progression de la meilleure fitness à chaque génération.

## Structure des fichiers

* `main.py` : Point d'entrée du programme. Définit la solution cible et lance l'algorithme.
* `simple_genetic_algorithm.py` : Contient la classe principale `SimpleGeneticAlgorithm` qui gère la logique d'évolution (sélection, crossover, mutation) et la boucle des générations.
* `population.py` : Définit la classe `Population`, qui est un conteneur pour un ensemble d'individus. Gère la création de la population initiale.
* `individual.py` : Définit la classe `Individual`. Chaque individu possède un génome (liste de gènes) et une méthode pour calculer sa propre `fitness`.
