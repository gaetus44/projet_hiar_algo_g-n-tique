import random

from individual import Individual

class Population:
    def __init__(self, size, initialize=True):
        # Liste qui contient tous les individus
        self.individuals = []
        if initialize:
            # Crée 'size' individus aléatoires
            for _ in range(size):
                random_gene = random.randint(32,128)
                individu=Individual(random_gene)
                self.individuals.append(individu)
                #print(individu)


    def get_individual(self, index):
        # Retourne l'individu à la position 'index'
        return self.individuals[index]

    def get_fittest(self, solution):
        # Retourne l'individu avec la meilleure fitness
        return max(self.individuals, key=lambda ind: ind.get_fitness(solution))

    def size(self):
        # Retourne le nombre d'individus
        return len(self.individuals)
