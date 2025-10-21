import random
#from encodings.punycode import generate_generalized_integer

from individual import Individual
from population import Population

class SimpleGeneticAlgorithm:

    def __init__(self, solution_string="0"*64, selection_type="tournament"):
        # Transforme la solution en liste de 0 et 1
        self.solution = [int(c) if c in "01" else 0 for c in solution_string]

        self.selection_type = selection_type

        if selection_type == "tournament":
            user_input = input("Nombre d'individus dans le tournoi ? [Défaut: 5]: ")
            self.tournament_size = int(user_input) if user_input else 5
        else:
            self.tournament_size = 5

        user_input = input("Probabilité de choisir les parents (ex: 0.5) ? [Défaut: 0.5]: ")
        self.uniform_rate = float(user_input) if user_input else 0.5

        user_input = input("Probabilité de mutation 'FLIP' (ex: 0.025) ? [Défaut: 0.025]: ")
        self.mutation_rate_flip = float(user_input) if user_input else 0.025

        user_input = input("Probabilité de mutation 'ADD' (ex: 0.01) ? [Défaut: 0.01]: ")
        self.mutation_rate_add = float(user_input) if user_input else 0.01

        user_input = input("Probabilité de mutation 'REMOVE' (ex: 0.01) ? [Défaut: 0.01]: ")
        self.mutation_rate_remove = float(user_input) if user_input else 0.01

        user_input = input("Activer l'élitisme (o/n) ? [Défaut: Oui]: ").lower()
        self.elitism = False if user_input == 'n' else True

        user_input = input("Nombre maximum de génération? [Défaut: 50]: ")
        self.max_gen = int(user_input) if user_input else 50


    def run_algorithm(self, population_size):
        # Crée la population initiale
        pop = Population(population_size, len(self.solution), True)
        generation_count = 1

        # Boucle jusqu'à ce que la solution soit trouvée
        while pop.get_fittest(self.solution).get_fitness(self.solution) < self.get_max_fitness() and generation_count <= self.max_gen:#valeur max du fittest est la taille de la chaine cible
            fittest = pop.get_fittest(self.solution)#cherche l'individu avec le plus haut fittest
            print(f"Generation: {generation_count} Correct genes found: {fittest.get_fitness(self.solution)}")
            # Évolue la population pour la prochaine génération
            pop = self.evolve_population(pop)#relance l'évolution de la population
            generation_count += 1

        generation_count-=1
        # Affiche le résultat final
        if generation_count <= self.max_gen:
            print(f"Generation: {generation_count}")
            print("Genes:")
            print(pop.get_fittest(self.solution))
            return True
        else:
            print("the algorithm is stagnating")
            print(f"Generation: {generation_count}")
            print("Genes:")
            print(pop.get_fittest(self.solution))
            return True

    def evolve_population(self, pop):#reproduire/muter/sélectionner
        #garde le meilleur individu si elitism est à true/crée de nouveau individus par crossover(reproduction)/applique une mutation aléatoire pour introduire la diversité
        # Nouvelle population videa
        new_pop = Population(pop.size(), initialize=False) #création d'une nouvelle population pour les enfants
        elitism_offset = 1 if self.elitism else 0

        # Garde le meilleur individu si élitisme activé
        if self.elitism:                        #garde le meilleur individu
            new_pop.individuals.append(pop.get_fittest(self.solution))#place le meilleure individu dans la nouvelle population

        # Remplit le reste de la population avec de nouveaux individus issus de crossover
        for i in range(elitism_offset, pop.size()):

            if self.selection_type == "tournament":

                # Sélection des deux parents
                indiv1 = self.tournament_selection(pop)
                indiv2 = self.tournament_selection(pop)

                # Assure que les parents sont différents
                while indiv1 is indiv2:
                    indiv2 = self.tournament_selection(pop)

            elif self.selection_type == "roulette":
                indiv1 = self.roulette_wheel_selection(pop)
                indiv2 = self.roulette_wheel_selection(pop)

                # Assure que les parents sont différents
                while indiv1 is indiv2:
                    indiv2 = self.tournament_selection(pop)

            # Crée l'enfant
            new_indiv = self.crossover(indiv1, indiv2)
            new_pop.individuals.append(new_indiv)

        # Applique la mutation à tous les individus sauf le meilleur si élitisme
        for i in range(elitism_offset, new_pop.size()):
            self.mutate(new_pop.get_individual(i))

        return new_pop

    def crossover(self, indiv1, indiv2):
        keep_fittest = False
        # Crée un enfant en mélangeant les gènes des deux parents

        shorter, longer = (indiv1, indiv2) if indiv1.get_length() < indiv2.get_length() else (indiv2, indiv1)

        child_genes = []

        for i in range(shorter.get_length()):
            if random.random() <= self.uniform_rate: #copie le gène du parent 1
                child_genes.append(indiv1.get_single_gene(i))
            else:#sinon copie le gène du parent 2 et fait ça pour les 64 bits
                child_genes.append(indiv2.get_single_gene(i))


        for i in range(shorter.get_length(), longer.get_length()):
            if not keep_fittest:
                #print("random")
                if random.random() < 0.5:                               # random (46 gen for "10101010101010101010101010101")
                    child_genes.append(longer.get_single_gene(i))
            else:
                #print("Keep additional bits only if they belong to fittest parent")
                if longer.get_fitness(self.solution) > shorter.get_fitness(self.solution):         # Keep additional bits only if they belong to fittest parent (1461 gen for "10101010101010101010101010101")
                    child_genes.append(longer.get_single_gene(i))
                    pass

        return Individual(genes_list=child_genes)

    def mutate(self, indiv):#réintroduire un peu de "hasard" dans la population un fois que la population est devenue trop "semblable" -> le croisement entre les parents très simulaires produisent toujours les mêmes enfants

        if random.random() <= self.mutation_rate_add:
            indiv.add_gene(random.choice([0, 1]))

        if indiv.get_length() > 0 and random.random() <= self.mutation_rate_remove:

            indiv.remove_gene(random.randint(0, indiv.get_length() - 1 ))

        for i in range(indiv.get_length()):
            if random.random() <= self.mutation_rate_flip:
                indiv.set_single_gene(i, 1 - indiv.get_single_gene(i))

    def tournament_selection(self, pop):
        # Sélectionne le meilleur individu parmi un sous-groupe aléatoire/roue pour sélectionner le parent
        tournament = Population(self.tournament_size, len(self.solution), initialize=False)
        for _ in range(self.tournament_size):
            random_indiv = pop.get_individual(random.randint(0, pop.size()-1))
            tournament.individuals.append(random_indiv)
        return tournament.get_fittest(self.solution)

    def roulette_wheel_selection(self, pop):
        # Calcule la fitness totale de la population
        total_fitness = sum(indiv.get_fitness(self.solution) for indiv in pop.individuals)

        # Gérer le cas où la fitness totale est nulle (pour éviter la division par zéro)
        if total_fitness == 0:
            # Si tout est à 0, retournez un individu au hasard
            return pop.get_individual(random.randint(0, pop.size() - 1))

        # Choisir un "point de sélection" aléatoire entre 0 et la fitness totale
        pick = random.uniform(0, total_fitness)

        # "Faire tourner la roue"
        current_fitness = 0
        for indiv in pop.individuals:
            current_fitness += indiv.get_fitness(self.solution)
            if current_fitness > pick:
                return indiv

        # En cas de problème d'arrondi, retourner le dernier
        return pop.individuals[-1]

    def get_max_fitness(self):
        # Fitness maximale = longueur de la solution
        return len(self.solution)
