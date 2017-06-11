#!/bin/python3

from simulated_annealing import simulated_annealing, target_function, calculate_nutrients
from config import CONFIG, generate_nutrient_functions
from meal_parser import MealParser
from out import out

if __name__ == '__main__':
    FOOD_PARSER = MealParser(CONFIG['FILE_NAME'])
    FOOD = FOOD_PARSER.read_meals_from_file()
    config = generate_nutrient_functions(CONFIG, CONFIG['NUTRIENTS_WEIGHTS'], CONFIG['GOAL'])
    BEST_DIET = simulated_annealing(config['DAYS_OF_DIET'], config['GOAL'], FOOD, config)
    out(FOOD,
        BEST_DIET,
        [g*config['DAYS_OF_DIET'] for g in config['GOAL']],
        target_function(BEST_DIET, config['GOAL'], FOOD, config),
        config
    )
