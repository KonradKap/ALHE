#!/bin/python3

from simulated_annealing import simulated_annealing, target_function, calculate_nutrients
from config import Config

if __name__ == '__main__':
    GOAL = [12, 13, 14, 15]
    FOOD = {'koks' : [0, 0, 0, 1234],  #SHOULD BE ORDERED_DICT
            'woda' : [100, 0, 0, 0],
            'polibuda' : [1, 1, 1, 1]}
    BEST_DIET = simulated_annealing(4, GOAL, FOOD, Config)
    print(BEST_DIET)
    print(calculate_nutrients(BEST_DIET, FOOD))
    print([g*4 for g in GOAL])
    print(target_function(BEST_DIET, GOAL, FOOD, Config))
