import random
from individual import Individual
from population import Population

class SimpleGeneticAlgorithm:
    user_input = input("Probabilité de choisir les parents (ex: 0.5) ? [Défaut: 0.5]: ")
    uniform_rate = float(user_input) if user_input else 0.5

    user_input = input("Probabilité de mutation (ex: 0.025) ? [Défaut: 0.025]: ")
    mutation_rate = float(user_input) if user_input else 0.025

    user_input = input("Nombre d'individus dans le tournoi ? [Défaut: 5]: ")
    tournament_size = int(user_input) if user_input else 5

    user_input = input("Activer l'élitisme (o/n) ? [Défaut: Oui]: ").lower()
    elitism = False if user_input == 'n' else True

    def __init__(self, solution_string="0"*64):
        # Transforme la solution en liste de 0 et 1
        self.solution = [int(c) if c in "01" else 0 for c in solution_string]


    def run_algorithm(self, population_size):
        # Crée la population initiale
        pop = Population(population_size, len(self.solution), True)
        generation_count = 1

        # Boucle jusqu'à ce que la solution soit trouvée
        while pop.get_fittest(self.solution).get_fitness(self.solution) < self.get_max_fitness():#valeur max du fittest est la taille de la chaine cible
            fittest = pop.get_fittest(self.solution)#cherche l'individu avec le plus haut fittest
            print(f"Generation: {generation_count} Correct genes found: {fittest.get_fitness(self.solution)}")
            # Évolue la population pour la prochaine génération
            pop = self.evolve_population(pop)#relance l'évolution de la population
            generation_count += 1

        # Affiche le résultat final
        print("Solution found!")
        print(f"Generation: {generation_count}")
        print("Genes:")
        print(pop.get_fittest(self.solution))
        return True

    def evolve_population(self, pop):#reproduire/muter/sélectionner
        #garde le meilleur individu si elitism est à true/crée de nouveau individus par crossover(reproduction)/applique une mutation aléatoire pour introduire la diversité
        # Nouvelle population videa
        new_pop = Population(pop.size(), len(self.solution), initialize=False)#création d'une nouvelle population pour les enfants
        elitism_offset = 1 if self.elitism else 0

        # Garde le meilleur individu si élitisme activé
        if self.elitism:                        #garde le meilleur individu
            new_pop.individuals.append(pop.get_fittest(self.solution))#place le meilleure individu dans la nouvelle population

        # Remplit le reste de la population avec de nouveaux individus issus de crossover
        for i in range(elitism_offset, pop.size()):
            # Sélection des deux parents
            indiv1 = self.tournament_selection(pop)
            indiv2 = self.tournament_selection(pop)

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
        # Crée un enfant en mélangeant les gènes des deux parents
        child = Individual(len(self.solution))
        for i in range(len(self.solution)):
            if random.random() <= self.uniform_rate: #copie le gène du parent 1
                child.set_single_gene(i, indiv1.get_single_gene(i))
            else:#sinon copie le gène du parent 2 et fait ça pour les 64 bits
                child.set_single_gene(i, indiv2.get_single_gene(i))
        return child

    def mutate(self, indiv):#réintroduire un peu de "hasard" dans la population un fois que la population est devenue trop "semblable" -> le croisement entre les parents très simulaires produisent toujours les mêmes enfants
        # Inverse aléatoirement certains gènes selon mutation_rate
        for i in range(len(self.solution)):
            if random.random() <= self.mutation_rate:
                indiv.set_single_gene(i, 1 - indiv.get_single_gene(i))

    def tournament_selection(self, pop):
        # Sélectionne le meilleur individu parmi un sous-groupe aléatoire/roue pour sélectionner le parent
        tournament = Population(self.tournament_size, len(self.solution), initialize=False)
        for _ in range(self.tournament_size):
            random_indiv = pop.get_individual(random.randint(0, pop.size()-1))
            tournament.individuals.append(random_indiv)
        return tournament.get_fittest(self.solution)

    def get_max_fitness(self):
        # Fitness maximale = longueur de la solution
        return len(self.solution)
