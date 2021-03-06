
from Initial import initial
import random, time

from Variation import CrossOver
from evaluate_solution import evaluate_singlefitness, evaluate_single
from copy import copy


def PMOEAD(file_name, dimension, population_size, max_iteration, begin, end):
    population, weight_vecotr, neighbours, obj, z, fitness, data = initial(population_size, dimension, file_name)
    iteration = 0
    negihbour_num = len(neighbours[0])
    while iteration < max_iteration:
        iteration += 1
        index = begin
        while index < end:
            p = random.sample(range(0, negihbour_num), 2)  # select two parents from its neighbour
            p1 = int(neighbours[index][p[0]])
            p2 = int(neighbours[index][p[1]])
            indiviual = CrossOver(population[p1], population[p2], dimension)
            i_obj = evaluate_single(indiviual, copy(data))
            if i_obj[0] < z[0]:
                z[0] = i_obj[0]
            if i_obj[1] < z[1]:
                z[1] = i_obj[1]
            update_neighbour(population, neighbours[index], indiviual, obj, fitness, weight_vecotr)
            index += 1
        # print(fiteration {iteration}'
        print("iteration:", iteration)
    return population, obj


def PMOEAD_bytime(file_name, dimension, population_size, max_time, begin, end):
    TIME = time.time()
    population, weight_vecotr, neighbours, obj, z, fitness, data = initial(population_size, dimension, file_name)
    iteration = 0
    negihbour_num = len(neighbours[0])
    while time.time() - TIME < max_time:
        iteration += 1
        index = begin
        while index < end:
            p = random.sample(range(0, negihbour_num), 2)  # select two parents from its neighbour
            p1 = int(neighbours[index][p[0]])
            p2 = int(neighbours[index][p[1]])
            indiviual = CrossOver(population[p1], population[p2], dimension)
            i_obj = evaluate_single(indiviual, copy(data))
            if i_obj[0] < z[0]:
                z[0] = i_obj[0]
            if i_obj[1] < z[1]:
                z[1] = i_obj[1]
            update_neighbour(population, neighbours[index], indiviual,i_obj, obj , fitness, weight_vecotr)
            index += 1
        # print(fiteration {iteration}'
        print("iteration:", iteration)
    return population, obj


def update_neighbour(population, neighbour, indiviual,i_obj, obj, fitness, weight_vector):
    s = sum(indiviual)
    population_num = len(population)
    for i in neighbour:
        index = int(i)
        temp = evaluate_singlefitness(obj[index][0], obj[index][1], s, int(weight_vector[index][0] * population_num))
        if fitness[index] > temp:
            population[index] = copy(indiviual)
            fitness[index] = temp
            obj[index][0] = i_obj[0]
            obj[index][1] = i_obj[1]

