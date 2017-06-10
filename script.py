#!/bin/python3

from simulated_annealing import simulated_annealing, target_function, calculate_nutrients
from config import CONFIG, generate_nutrient_functions, generate_cooling_rate
from config import FILE_NAME
from meal_parser import MealParser
DAYS_OF_DIET = 10

if __name__ == '__main__':
    GOAL = [2500, 60, 340, 80]
    FOOD_PARSER = MealParser(FILE_NAME)
    FOOD = FOOD_PARSER.read_meals_from_file()
    print(FOOD)

    config = generate_nutrient_functions(CONFIG, CONFIG['NUTRIENTS_WEIGHTS'], GOAL)
    generate_cooling_rate(config)
    BEST_DIET = simulated_annealing(DAYS_OF_DIET, GOAL, FOOD, config)
    print(BEST_DIET)
    print(calculate_nutrients(BEST_DIET, FOOD))
    print([g*DAYS_OF_DIET for g in GOAL])
    print(target_function(BEST_DIET, GOAL, FOOD, config))
