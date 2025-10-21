import random
import math

class Individual:
    def __init__(self, gene_length=64, genes_list=None):
        if genes_list:
            self.genes = list(genes_list)
        else:
            # Génère aléatoirement un individu avec des 0 et 1
            self.genes = [random.choice([0, 1]) for _ in range(gene_length)]

        # Fitness = nombre de gènes corrects par rapport à la solution
        self.fitness = 0

    def get_length(self):
        return len(self.genes)

    def get_single_gene(self, index):
        # Retourne le gène à l'index donné
        return self.genes[index]

    def set_single_gene(self, index, value):
        # Modifie le gène à l'index donné
        self.genes[index] = value
        # Réinitialise la fitness, car l'individu a changé
        self.fitness = 0

    def add_gene(self, value):
        self.genes.append(value)
        self.fitness = 0

    def remove_gene(self, index):
        if self.get_length() > 0:
            self.genes.pop(index)
            self.fitness = 0


    def get_fitness(self, solution):

        if self.fitness == 0:
            solution_len = len(solution)
            indiv_len = self.get_length()
            common_len = min(solution_len, indiv_len)

            # bits correspondants
            matching_bits = sum(1 for i in range(common_len) if self.genes[i] == solution[i])

            length_difference = abs(solution_len - indiv_len)
            penalty = length_difference * 0.5

            # fitness finale
            self.fitness = math.floor(max(0, matching_bits - penalty))


        return self.fitness

    def __str__(self):
        # Transforme les gènes en chaîne de 0 et 1 pour affichage
        return ''.join(map(str, self.genes))
