import random

from individual import Individual
from population import Population

class SimpleGeneticAlgorithm:
    """
    Classe principale implémentant l'algorithme génétique simple.
    Gère l'évolution d'une population pour trouver une solution binaire cible.
    """
    def __init__(self, solution_string="0"*64, selection_type="tournament"):
        """
        Initialise l'algorithme avec les paramètres.
        'solution_string' : La chaîne cible que l'AG doit trouver.
        'selection_type' : La méthode de sélection ("tournament" ou "roulette").
        """

        # Transforme la solution (chaîne) en liste d'entiers (0 et 1)
        self.solution = [int(c) if c in "01" else 0 for c in solution_string]

        self.selection_type = selection_type

        # Configuration des paramètres via des entrées utilisateur (avec valeurs par défaut)
        if selection_type == "tournament":
            # Taille du tournoi pour la sélection
            user_input = input("Nombre d'individus dans le tournoi ? [Défaut: 5]: ")
            self.tournament_size = int(user_input) if user_input else 5
        else:
            self.tournament_size = 5 # Valeur par défaut si non-tournoi 

        # Taux d'uniformité pour le crossover (probabilité de prendre le gène du parent 1)
        user_input = input("Probabilité de choisir les parents (ex: 0.5) ? [Défaut: 0.5]: ")
        self.uniform_rate = float(user_input) if user_input else 0.5

        # Taux de mutation 'FLIP' (inverser un bit)
        user_input = input("Probabilité de mutation 'FLIP' (ex: 0.025) ? [Défaut: 0.025]: ")
        self.mutation_rate_flip = float(user_input) if user_input else 0.025

        # Taux de mutation 'ADD' (ajouter un bit)
        user_input = input("Probabilité de mutation 'ADD' (ex: 0.01) ? [Défaut: 0.01]: ")
        self.mutation_rate_add = float(user_input) if user_input else 0.01

        # Taux de mutation 'REMOVE' (supprimer un bit)
        user_input = input("Probabilité de mutation 'REMOVE' (ex: 0.01) ? [Défaut: 0.01]: ")
        self.mutation_rate_remove = float(user_input) if user_input else 0.01

        # Activation de l'élitisme (garder le meilleur individu à chaque génération)
        user_input = input("Activer l'élitisme (o/n) ? [Défaut: Oui]: ").lower()
        self.elitism = False if user_input == 'n' else True

        # Nombre maximum de générations (condition d'arrêt pour éviter une boucle infinie)
        user_input = input("Nombre maximum de génération? [Défaut: 50]: ")
        self.max_gen = int(user_input) if user_input else 50


    def run_algorithm(self, population_size):
        """
        Lance l'exécution de l'algorithme génétique.
        'population_size' : La taille de la population à utiliser.
        """
        
        # Crée la population initiale
        pop = Population(population_size, True)
        generation_count = 1

        # Boucle d'évolution : continue tant que la meilleure fitness est inférieure à la fitness maximale
        # (longueur de la solution) ET que le nombre max de générations n'est pas atteint.
        while pop.get_fittest(self.solution).get_fitness(self.solution) < self.get_max_fitness() and generation_count <= self.max_gen:#valeur max du fittest est la taille de la chaine cible
            
            # Récupère le meilleur individu de la génération actuelle
            fittest = pop.get_fittest(self.solution)#cherche l'individu avec le plus haut fittest
            print(f"Generation: {generation_count} Correct genes found: {fittest.get_fitness(self.solution)}")

            # Fait évoluer la population pour créer la prochaine génération
            pop = self.evolve_population(pop)
            generation_count += 1 

        generation_count-=1 # Ajuste le compteur pour afficher la dernière génération traitée
        
        # Affiche le résultat final
        if generation_count <= self.max_gen:
            print(f"Generation: {generation_count}")
            print("Genes:")
            print(pop.get_fittest(self.solution))
            return True
        else:
            # Si on atteint max_gen sans trouver la solution
            print("the algorithm is stagnating")
            print(f"Generation: {generation_count}")
            print("Genes:")
            print(pop.get_fittest(self.solution))
            return True

    def evolve_population(self, pop):#reproduire/muter/sélectionner
        """
        Crée une nouvelle génération à partir de la population 'pop'
        en appliquant sélection, crossover et mutation.
        """
        
        # Nouvelle population vide (taille identique à l'ancienne)
        new_pop = Population(pop.size(), initialize=False) 
        
        # 'elitism_offset' : 1 si l'élitisme est activé (on réserve une place), 0 sinon.
        elitism_offset = 1 if self.elitism else 0

        # 1. ÉLITISME
        # Si l'élitisme est activé, on copie le meilleur individu directement dans la nouvelle génération
        if self.elitism:                        #garde le meilleur individu
            new_pop.individuals.append(pop.get_fittest(self.solution))#place le meilleure individu dans la nouvelle population

        # 2. CROSSOVER (Reproduction)
        # Remplit le reste de la population avec des enfants issus du crossover
        for i in range(elitism_offset, pop.size()):

            if self.selection_type == "tournament":

                # Sélection des deux parents selon la méthode choisie
                indiv1 = self.tournament_selection(pop)
                indiv2 = self.tournament_selection(pop)

                # Assure que les parents sont différents (simple vérification)
                while indiv1 is indiv2:
                    indiv2 = self.tournament_selection(pop)

            elif self.selection_type == "roulette":
                indiv1 = self.roulette_wheel_selection(pop)
                indiv2 = self.roulette_wheel_selection(pop)

                # Assure que les parents sont différents
                while indiv1 is indiv2:
                    indiv2 = self.roulette_wheel_selection(pop)

            # Crée l'enfant par crossover
            new_indiv = self.crossover(indiv1, indiv2)
            new_pop.individuals.append(new_indiv)

        # 3. MUTATION
        # Applique la mutation à tous les individus de la nouvelle population,
        # SAUF au meilleur (l'élite) si l'élitisme est activé (commence à 'elitism_offset').
        for i in range(elitism_offset, new_pop.size()):
            self.mutate(new_pop.get_individual(i))

        return new_pop

    def crossover(self, indiv1, indiv2):
        """
        Effectue un crossover (uniforme) entre deux parents (indiv1, indiv2)
        pour créer un nouvel individu (enfant).
        Gère aussi les génomes de longueurs différentes.
        """
        keep_fittest = True # Option pour la gestion des gènes excédentaires
        
        # Crée un enfant en mélangeant les gènes des deux parents

        # Identifie le parent le plus court et le plus long
        shorter, longer = (indiv1, indiv2) if indiv1.get_length() < indiv2.get_length() else (indiv2, indiv1)

        child_genes = []

        # Partie 1: Crossover uniforme sur la longueur commune
        # Pour chaque gène, on choisit aléatoirement celui du parent 1 ou 2
        for i in range(shorter.get_length()):
            if random.random() <= self.uniform_rate: 
                # Prend le gène du parent 1
                child_genes.append(indiv1.get_single_gene(i))
            else:
                # Prend le gène du parent 2
                child_genes.append(indiv2.get_single_gene(i))

        # Partie 2: Gestion des gènes excédentaires (du parent le plus long)
        for i in range(shorter.get_length(), longer.get_length()):
            if not keep_fittest:
                # Option 1 (désactivée) : 50% de chance de garder le gène excédentaire
                if random.random() < 0.5:                              
                    child_genes.append(longer.get_single_gene(i))
            else:
                # Option 2 (activée) : Garde les gènes excédentaires SEULEMENT
                # s'ils proviennent du parent ayant la meilleure fitness.
                if longer.get_fitness(self.solution) > shorter.get_fitness(self.solution):
                    child_genes.append(longer.get_single_gene(i))

        # Crée le nouvel individu avec les gènes résultants
        return Individual(genes_list=child_genes)

    def mutate(self, indiv):
        """
        Applique trois types de mutations à un individu, chacune avec sa propre probabilité.
        Permet d'introduire de la diversité génétique.
        """

        # Mutation 1: ADD (Ajouter un gène)
        if random.random() <= self.mutation_rate_add:
            indiv.add_gene(random.choice([0, 1])) # Ajoute 0 ou 1 à la fin

        # Mutation 2: REMOVE (Supprimer un gène)
        # S'applique seulement si l'individu a au moins un gène
        if indiv.get_length() > 0 and random.random() <= self.mutation_rate_remove:

            indiv.remove_gene(random.randint(0, indiv.get_length() - 1 )) # Supprime un gène au hasard

        # Mutation 3: FLIP (Inverser un gène)
        # Parcourt tous les gènes de l'individu
        for i in range(indiv.get_length()):
            # Si le nombre aléatoire est inférieur au taux de mutation...
            if random.random() <= self.mutation_rate_flip:
                # Inverse le gène (0 devient 1, 1 devient 0)
                indiv.set_single_gene(i, 1 - indiv.get_single_gene(i))

    def tournament_selection(self, pop):
        """
        Sélectionne un individu parent par la méthode du tournoi.
        On choisit 'tournament_size' individus au hasard, et le meilleur gagne.
        """
        
        # Crée une "population" temporaire pour le tournoi
        tournament = Population(self.tournament_size, initialize=False)
        
        # Remplit le tournoi avec des individus choisis au hasard dans la population principale
        for _ in range(self.tournament_size):
            random_indiv = pop.get_individual(random.randint(0, pop.size()-1))
            tournament.individuals.append(random_indiv)

        # Retourne le meilleur individu (le gagnant) du tournoi
        return tournament.get_fittest(self.solution)

    def roulette_wheel_selection(self, pop):
        """
        Sélectionne un individu parent par la méthode de la roue de la fortune (Roulette Wheel).
        Les individus avec une meilleure fitness ont plus de chances d'être sélectionnés.
        """
        
        # Calcule la fitness totale de la population
        total_fitness = sum(indiv.get_fitness(self.solution) for indiv in pop.individuals)

        # Gérer le cas où la fitness totale est nulle (pour éviter la division par zéro)
        if total_fitness == 0:
            # Si toutes les fitness sont à 0, on retourne un individu au hasard
            return pop.get_individual(random.randint(0, pop.size() - 1))

        # Choisir un "point de sélection" aléatoire entre 0 et la fitness totale
        pick = random.uniform(0, total_fitness)

        # "Faire tourner la roue" : parcourir les individus et accumuler leur fitness
        current_fitness = 0
        for indiv in pop.individuals:
            current_fitness += indiv.get_fitness(self.solution)
            # Si la fitness accumulée dépasse le point de sélection, on choisit cet individu
            if current_fitness > pick:
                return indiv

        # En cas de problème d'arrondi (très rare), retourner le dernier individu
        return pop.individuals[-1]

    def get_max_fitness(self):
        """
        Retourne la fitness maximale possible.
        Dans ce problème, c'est simplement la longueur de la solution cible.
        """
        return len(self.solution)
