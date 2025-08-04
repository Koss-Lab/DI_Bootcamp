#DailyChallengeGold.py

import random

class Gene:
    def __init__(self):
        self.value = random.choice([0, 1])

    def mutate(self):
        if random.random() < 0.5:
            self.value = 1 - self.value

    def force_mutate(self):
        self.value = 1

    def __str__(self):
        return str(self.value)

class Chromosome:
    def __init__(self):
        self.genes = [Gene() for _ in range(10)]

    def mutate(self):
        for gene in self.genes:
            if random.random() < 0.5:
                gene.mutate()

    def force_mutate(self):
        for gene in self.genes:
            gene.force_mutate()

    def is_full_one(self):
        return all(g.value == 1 for g in self.genes)

    def __str__(self):
        return "".join(str(g) for g in self.genes)

class DNA:
    def __init__(self):
        self.chromosomes = [Chromosome() for _ in range(10)]

    def mutate(self):
        for chromosome in self.chromosomes:
            if random.random() < 0.5:
                chromosome.mutate()

    def force_mutate(self):
        for chromosome in self.chromosomes:
            chromosome.force_mutate()

    def is_perfect(self):
        return all(c.is_full_one() for c in self.chromosomes)

    def __str__(self):
        return "\n".join(str(c) for c in self.chromosomes)

class Organism:
    def __init__(self, dna, environment=0.9):
        self.dna = dna
        self.environment = environment

    def mutate(self):
        if random.random() < self.environment:
            self.dna.mutate()

    def force_mutate(self):
        self.dna.force_mutate()

if __name__ == "__main__":
    generations = 0
    organism = Organism(DNA(), environment=1.0)

    while not organism.dna.is_perfect():
        organism.mutate()
        generations += 1
        if generations % 100000 == 0:
            print(f"Generation {generations}... still mutating")

        # Pour accélérer si trop long
        if generations > 2000000:
            organism.force_mutate()
            generations += 1
            break

    print("✅ All genes are 1!")
    print("Final DNA:\n")
    print(organism.dna)
    print(f"\n🧬 Total generations to reach perfection: {generations}")
