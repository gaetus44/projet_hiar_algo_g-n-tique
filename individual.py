import random

class Individual:
    def __init__(self, gene_length=64):
        # Taille de l'ADN (nombre de gènes)
        self.gene_length = gene_length
        # Génère aléatoirement un individu avec des 0 et 1
        self.genes = [random.choice([0, 1]) for _ in range(gene_length)]
        # Fitness = nombre de gènes corrects par rapport à la solution
        self.fitness = 0

    def get_single_gene(self, index):
        # Retourne le gène à l'index donné
        return self.genes[index]

    def set_single_gene(self, index, value):
        # Modifie le gène à l'index donné
        self.genes[index] = value
        # Réinitialise la fitness, car l'individu a changé
        self.fitness = 0

    def get_fitness(self, solution):
        # Calcule la fitness si elle n'est pas déjà calculée
        if self.fitness == 0:
            # Compte le nombre de gènes identiques à la solution
            self.fitness = sum(1 for i in range(self.gene_length) if self.genes[i] == solution[i])
        return self.fitness

    def __str__(self):
        # Transforme les gènes en chaîne de 0 et 1 pour affichage
        return ''.join(map(str, self.genes))
