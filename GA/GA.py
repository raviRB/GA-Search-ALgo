import random
import copy
import math
import numpy as np


# this function calculates number of attacking pairs
def fitness(individual):
    cur_fitness = 0
    for i in range(len(individual)):
        # check for attack in same column
        for j in range(len(individual)):
            if j != i and individual[i] == individual[j]:
                cur_fitness += 1
        # check for attack in diagonals
        for j in range(len(individual)):
            if i != j and abs(i - j) == abs(individual[i] - individual[j]):
                cur_fitness += 1
    return cur_fitness


def crossover(individual1, individual2):
    # randomly choose a position to split
    split_point = random.randint(1, len(individual1) - 1)
    child_1, child_2 = individual1[:split_point], individual2[:split_point]
    for i in range(split_point, len(individual2)):
        child_1.append(individual2[i])
        child_2.append(individual1[i])
    return child_1, child_2


def mutation(individual):
    rep = int(math.sqrt(len(individual)))
    # rep is the number of bits that will be mutated
    for i in range(rep):
        individual[random.randint(0, len(individual) - 1)] = random.randint(1, len(individual))
    return individual


def generate_individual(n):
    result = list(range(1, n + 1))
    np.random.shuffle(result)
    return result


class Genetic(object):

    def __init__(self, n, pop_size):
        # initializing a random individuals with size of initial population entered by user
        self.queens = []
        for i in range(pop_size):
            self.queens.append(generate_individual(n))

    # generating individuals for a single iteration of algorithm
    def generate_population(self, random_selections=5):
        candid_parents = []
        candid_fitness = []
        # getting individuals from queens randomly for an iteration
        for i in range(random_selections):
            candid_parents.append(self.queens[random.randint(0, len(self.queens) - 1)])
            candid_fitness.append(fitness(candid_parents[i]))
        sorted_fitness = copy.deepcopy(candid_fitness)
        # sort the fitnesses of individuals
        sorted_fitness.sort()
        # getting 2 first individuals(min attackings)
        first_individual = candid_parents[candid_fitness.index(sorted_fitness[0])]
        second_individual = candid_parents[candid_fitness.index(sorted_fitness[1])]
        # crossover the two parents
        crossover_prob = 0.9
        mutation_prob = 0.09
        if random.random() <= crossover_prob:
            child_1, child_2 = crossover(first_individual, second_individual)
        else:
            child_1, child_2 = first_individual, second_individual
        # mutation
        if random.random() <= mutation_prob:
            child_1 = mutation(child_1)

        if random.random() <= mutation_prob:
            child_2 = mutation(child_2)
        # in code below check if each child is better than each one of queens individuals, set that individual the new child
        # finding the index of the individual in queens who has the worst fitness and replacing it with the child
        child_fitness = fitness(child_1)
        index = -1
        for i in range(len(self.queens)):
            if child_fitness <= fitness(self.queens[i]):
                index, child_fitness = i, fitness(self.queens[i])
            if index != -1:
                self.queens[index] = child_1

        child_fitness = fitness(child_2)
        index = -1
        for i in range(len(self.queens)):
            if child_fitness <= fitness(self.queens[i]):
                index, child_fitness = i, fitness(self.queens[i])
            if index != -1:
                self.queens[index] = child_2

    def finished(self):
        for i in self.queens:
            if fitness(i) == 0:
                return True, i
            # we check if for each queen there is no attacking(cause this algorithm should work for n queen,
            # it was easier to use attacking pairs for fitness instead of non-attacking)
        return [False]

    def start(self, random_selections=5):
        # generate new population and start algorithm until number of attacking pairs is zero
        while not self.finished()[0]:
            self.generate_population(random_selections)
        final_state = self.finished()
        print(('Solution : ' + str(final_state[1])))


# ******************** N-Queen Problem With GA Algorithm ***********************

n = (int)(input('Enter the value of N \n -'))
initial_population = (int)(input('Enter initial population size \n -'))

algorithm = Genetic(n=n, pop_size=initial_population)
algorithm.start()
