from simple_genetic_algorithm import SimpleGeneticAlgorithm

if __name__ == "__main__":
    solution = "1010101010101010101010101010101010101010101010101010101010101010"
    ga = SimpleGeneticAlgorithm(solution)
    ga.run_algorithm(50)


