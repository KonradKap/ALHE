#!/bin/python3

import itertools
import math
import sys
from enum import Enum

from simulated_annealing import target_function, simulated_annealing, calculate_nutrients
from meal_parser import MealParser

GOAL = [2500, 60, 340, 80]
MEAL_PARSER = MealParser('resources/csv.csv')
FOOD = MEAL_PARSER.read_meals_from_file()
DAYS = 10
REPEATS = 1

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

class Function:
    def __init__(self, function, params, type_):
        self.function = function
        self.params = params
        self.type_ = type_

    def __str__(self):
        return self.type_.format(*self.params)

def generate_functions():
    linear_functions = [Function(lambda x: -a*x, [-a], '{}*x')
                        for a in range(-5, 0)]
    logarithmic_functions = [Function(lambda x: a*math.log(abs(x) if x != 0 else 0.1), [a], '{}*log(x)')
                             for a in range(-5, 0)]
    square_functions = [Function(lambda x: a*x*x + b*x, [a, b], '{}*x^2 + {}*x')
                        for a in range(-5, 0)
                        for b in range(-3, 4) if b != 0]
    return linear_functions + logarithmic_functions + square_functions

def main():
    sys.stdout = Unbuffered(sys.stdout)
    functions = generate_functions()
    for variety, nutrients in itertools.product(functions, functions):
        results = []
        for i in range(REPEATS):
            class ConfigMock(Enum):
                VARIETY_WEIGHT = variety.function
                NUTRIENTS_WEIGHTS = [nutrients.function] * 4
                MAX_ITERATIONS = 1000

            print()
            print(i)
            print('variety:', str(variety))
            print('nutrients:', str(nutrients))
            DIET = simulated_annealing(DAYS, GOAL, FOOD, ConfigMock)
            print(DIET)
            print(calculate_nutrients(DIET, FOOD))
            print([g*DAYS for g in GOAL])
            results.append(target_function(DIET, GOAL, FOOD, ConfigMock))
            print(results[-1])
        print(">>>AVERAGED: {}".format(sum(results)/len(results)))

if __name__ == '__main__':
    main()
