import random

from individual import Individual

class Population:
    """
    Représente un ensemble d'individus.
    """
    def __init__(self, size, initialize=True):
        """
        Initialise la population.
        'size' : le nombre d'individus dans la population.
        'initialize' (bool) : si True, crée 'size' nouveaux individus aléatoires.
                               si False, crée une population vide (utile pour la nouvelle génération).
        """
        
        # Liste qui contient tous les individus
        self.individuals = []
        if initialize:
            # Crée 'size' individus aléatoires
            for _ in range(size):

                # Génère une longueur aléatoire pour le génome (entre 32 et 128)
                random_gene = random.randint(32,128)
                individu=Individual(random_gene)
                self.individuals.append(individu)


    def get_individual(self, index):
        """Retourne l'individu à la position 'index' dans la liste."""
        return self.individuals[index]

    def get_fittest(self, solution):
        """
        Retourne l'individu avec la meilleure fitness (la plus élevée)
        par rapport à la 'solution' donnée.
        """
        # Utilise max() avec une fonction lambda pour déterminer la clé de comparaison (la fitness)
        return max(self.individuals, key=lambda ind: ind.get_fitness(solution))

    def size(self):
        """Retourne le nombre d'individus (la taille) de la population."""
        return len(self.individuals)
