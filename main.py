from simple_genetic_algorithm import SimpleGeneticAlgorithm

if __name__ == "__main__":
    # Définition de la chaîne binaire cible (la solution) que l'algorithme doit trouver.
    solution = "1010101010101010101010101010101010101010101010101010101010101010"
    
    # Initialisation de l'algorithme génétique.
    # On passe la solution cible et le type de sélection (ici, "tournament").
    # D'autres options comme "roulette" sont possibles (comme indiqué dans le constructeur de SimpleGeneticAlgorithm).
    ga = SimpleGeneticAlgorithm(solution, selection_type="tournament") # tournament - roulette

    # Lancement de l'algorithme avec une population de 50 individus.
    ga.run_algorithm(50)

