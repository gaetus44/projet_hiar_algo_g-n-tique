import random
import math

class Individual:
    """
    Représente un individu dans la population de l'algorithme génétique.
    Un individu est caractérisé par son génome (une liste de gènes, ici 0 ou 1).
    """
    def __init__(self, gene_length=64, genes_list=None):
        """
        Initialise un individu.
        Soit en générant un génome aléatoire d'une longueur donnée (gene_length),
        soit en utilisant une liste de gènes fournie (genes_list).
        """
        if genes_list:
            # Utilise la liste de gènes fournie (ex: pour un enfant issu d'un crossover)
            self.genes = list(genes_list)
        else:
            # Génère aléatoirement un individu avec des 0 et 1
            self.genes = [random.choice([0, 1]) for _ in range(gene_length)]

        # Fitness = score de l'individu (ici, nombre de gènes corrects).
        # Initialisée à 0, elle sera calculée au besoin et mise en cache.
        self.fitness = 0

    def get_length(self):
        """Retourne la longueur (nombre de gènes) de l'individu."""
        return len(self.genes)

    def get_single_gene(self, index):
        """Retourne le gène (0 ou 1) à l'index donné."""
        return self.genes[index]

    def set_single_gene(self, index, value):
        """Modifie le gène à l'index donné."""
        self.genes[index] = value
        
        # Réinitialise la fitness, car l'individu a changé et son score doit être recalculé.
        self.fitness = 0

    def add_gene(self, value):
        """Ajoute un gène à la fin du génome de l'individu (mutation 'ADD')."""
        self.genes.append(value)
        
        # Réinitialise la fitness.
        self.fitness = 0

    def remove_gene(self, index):
        """Supprime un gène à l'index donné (mutation 'REMOVE'), si le génome n'est pas vide."""
        if self.get_length() > 0:
            self.genes.pop(index)
            
            # Réinitialise la fitness.
            self.fitness = 0


    def get_fitness(self, solution):
        """
        Calcule et retourne la fitness de l'individu par rapport à la solution cible.
        La fitness est mise en cache pour éviter les recalculs inutiles.
        """
        
        # Si la fitness n'a pas été calculée (ou a été réinitialisée)
        if self.fitness == 0:
            solution_len = len(solution)
            indiv_len = self.get_length()
            
            # Longueur commune pour la comparaison (le min des deux longueurs)
            common_len = min(solution_len, indiv_len)

            # Calcule le nombre de bits correspondants
            matching_bits = sum(1 for i in range(common_len) if self.genes[i] == solution[i])

            # Calcule une pénalité basée sur la différence de longueur
            length_difference = abs(solution_len - indiv_len)
            penalty = length_difference * 0.5

            # La fitness finale est le nombre de bits correspondants moins la pénalité.
            # On utilise math.floor pour avoir un entier et max(0, ...) pour ne pas avoir de fitness négative.
            self.fitness = math.floor(max(0, matching_bits - penalty))

        # Retourne la fitness (calculée ou mise en cache)
        return self.fitness

    def __str__(self):
        """Transforme les gènes en chaîne de 0 et 1 pour un affichage lisible."""
        return ''.join(map(str, self.genes))
