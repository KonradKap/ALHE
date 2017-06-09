#!/bin/python3

from simulated_annealing import simulated_annealing, target_function, calculate_nutrients
from config import Config
from config import FILE_NAME
from meal_parser import MealParser
DAYS_OF_DIET = 30

if __name__ == '__main__':
    GOAL = [2500, 60, 340, 80]
    FOOD_PARSER = MealParser(FILE_NAME)
    FOOD = FOOD_PARSER.read_meals_from_file()
    print(FOOD)

    # FOOD = {'koks' : [0, 0, 0, 1234],  #SHOULD BE ORDERED_DICT
    #         'woda' : [100, 0, 0, 0],
    #         'polibuda' : [1, 1, 1, 1]}
    BEST_DIET = simulated_annealing(DAYS_OF_DIET, GOAL, FOOD, Config)
    print(BEST_DIET)
    print(calculate_nutrients(BEST_DIET, FOOD))
    print([g*DAYS_OF_DIET for g in GOAL])
    print(target_function(BEST_DIET, GOAL, FOOD, Config))
