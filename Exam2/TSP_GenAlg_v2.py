#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 13:17:33 2021

@author: fieldstd
"""


import numpy as np
import matplotlib.pyplot as plt
from astar_function_py3 import astar
import time
import pylab as pl # Needed for plotting numbers on plots
#%matplotlib inline
#%config InlineBackend.figure_format = 'svg'
plt.style.use("seaborn")
np.random.seed(42)

class path_store:
    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        self.cost = cost

# Traveling Salesman Problem Example #
#       5 Desired Waypoints

gx = [0, 1, 2, 9, 9] # 5 desired waypoints
gy = [0, 9, 5, 9, 2]

sx = 0 # Starting point
sy = 0

#ox = [1, 2, 3, 4, 6, 7, 7] # List of obstacles in the graph
#oy = [7, 7, 7, 7, 2, 2, 3]

ox = [2, 3, 4, 4, 4, 4, 10, 9, 8, 7, 6, 6]
oy = [7, 7, 7, 8, 9, 10, 5, 5, 5, 5, 5, 4]
      
grid_size = 0.5
grid_x = 10
grid_y = 10
min_x = 0
min_y = 0

# Plotting   
plt.plot(ox, oy, ".b")
plt.plot(sx, sy, "xg")
plt.plot(gx, gy, "xr")
plt.axis([min_x, grid_x, min_y, grid_y])
plt.show()

# Initialize a cost matrix (distance cost to/from each waypoint)
cost_matrix = np.zeros([len(gx), len(gx)])
path_matrix = dict()

t = time.time()
# Brute force computing the cost from one waypoint to the next
for i in range(0,len(gx)):
    for j in range(0,len(gx)): # Skip a to a estimate
        if i!=j:
            print(gx[i],gy[i],gx[j],gy[j])
            temp_path_x, temp_path_y, temp_cost = astar(gx[i],gy[i],gx[j],gy[j],grid_x,grid_y,min_x,min_y,ox,oy,grid_size)
        
            path_matrix[i,j] = path_store(temp_path_x, temp_path_y, temp_cost)
            cost_matrix[i,j] = temp_cost
elapsed_time = time.time() - t



cities = [0, 1, 2, 3, 4]

adjacency_mat = cost_matrix

class Population():
    def __init__(self, bag, adjacency_mat):
        self.bag = bag
        self.parents = []
        self.score = 0
        self.best = None
        self.adjacency_mat = adjacency_mat

def init_population(cities, adjacency_mat, n_population):
    return Population(
        np.asarray([np.random.permutation(cities) for _ in range(n_population)]), 
        adjacency_mat
    )

pop = init_population(cities, adjacency_mat, 5)

def fitness(self, chromosome):
    return sum(
        [
            self.adjacency_mat[chromosome[i], chromosome[i + 1]]
            for i in range(len(chromosome) - 1)
        ]
    )

Population.fitness = fitness

def evaluate(self):
    distances = np.asarray(
        [self.fitness(chromosome) for chromosome in self.bag]
    )
    self.score = np.min(distances)
    self.best = self.bag[distances.tolist().index(self.score)]
    self.parents.append(self.best)
    if False in (distances[0] == distances):
        distances = np.max(distances) - distances
    return distances / np.sum(distances)
    
Population.evaluate = evaluate

def select(self, k=4):
    fit = self.evaluate()
    while len(self.parents) < k:
        idx = np.random.randint(0, len(fit))
        if fit[idx] > np.random.rand():
            self.parents.append(self.bag[idx])
    self.parents = np.asarray(self.parents)

Population.select = select

def swap(chromosome):
    a, b = np.random.choice(len(chromosome), 2)
    chromosome[a], chromosome[b] = (
        chromosome[b],
        chromosome[a],
    )
    return chromosome

def crossover(self, p_cross=0.1):
    children = []
    count, size = self.parents.shape
    for _ in range(len(self.bag)):
        if np.random.rand() > p_cross:
            children.append(
                list(self.parents[np.random.randint(count, size=1)[0]])
            )
        else:
            parent1, parent2 = self.parents[
                np.random.randint(count, size=2), :
            ]
            idx = np.random.choice(range(size), size=2, replace=False)
            start, end = min(idx), max(idx)
            child = [None] * size
            for i in range(start, end + 1, 1):
                child[i] = parent1[i]
            pointer = 0
            for i in range(size):
                if child[i] is None:
                    while parent2[pointer] in child:
                        pointer += 1
                    child[i] = parent2[pointer]
            children.append(child)
    return children

Population.crossover = crossover

def mutate(self, p_cross=0.1, p_mut=0.1):
    next_bag = []
    children = self.crossover(p_cross)
    for child in children:
        if np.random.rand() < p_mut:
            next_bag.append(swap(child))
        else:
            next_bag.append(child)
    return next_bag
    
Population.mutate = mutate



def genetic_algorithm(
    cities,
    adjacency_mat,
    n_population=500,
    n_iter=2000,
    selectivity=0.75,
    p_cross=0.5,
    p_mut=0.3,
    print_interval=100,
    return_history=False,
    verbose=False,
):
    pop = init_population(cities, adjacency_mat, n_population)
    best = pop.best
    score = float("inf")
    history = []
    for i in range(n_iter):
        pop.select(n_population * selectivity)
        history.append(pop.score)
        if verbose:
            print(f"Generation {i}: {pop.score}")
        elif i % print_interval == 0:
            print(f"Generation {i}: {pop.score}")
        if pop.score < score:
            best = pop.best
            score = pop.score
        children = pop.mutate(p_cross, p_mut)
        pop = Population(children, pop.adjacency_mat)
    if return_history:
        return best, history
    return best

best = genetic_algorithm(cities, adjacency_mat, verbose=False)

# Plotting   
plt.plot(ox, oy, ".b")
plt.plot(sx, sy, "xg")
plt.plot(gx, gy, "xr")
plt.axis([min_x-grid_size, grid_x+grid_size, min_y-grid_size, grid_y+grid_size])

for i in range(1,len(best)):
    plt.plot(path_matrix[best[i-1],best[i]].x,path_matrix[best[i-1],best[i]].y,'r-')
#plt.plot(pathx, pathy, "-r")
plt.xlabel('X Distance')
plt.ylabel('Y Distance')
plt.show()





