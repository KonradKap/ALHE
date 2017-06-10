#!/bin/python3

import itertools
import unittest
import math
import matplotlib.pyplot as plt

from argparse import Namespace
from collections import OrderedDict, defaultdict
from copy import deepcopy
from random import randint, random
from enum import Enum

from config import get_plot_name

_PLOT_POINTS = []

def simulated_annealing(number_of_days, goal, food, config):
    current = _get_starting_point(number_of_days, len(food))
    for i in range(1, config['MAX_ITERATIONS'] + 1):
        temperature = config['TEMPERATURE'] / float(i)
        current = _make_move(current, temperature, goal, food, config)

    plt.plot(_PLOT_POINTS)
    plt.savefig(get_plot_name(config))
    return current

def target_function(diet, goal, food, config):
    eaten_per_day = _get_eaten_per_day(diet, food)
    daily = sum(_evaluate_day(day, goal, config['NUTRIENTS_WEIGHTS']) for day in eaten_per_day)
    variety = sum(_evaluate_variety(day, config['VARIETY_WEIGHT']) for day in zip(*diet))
    period = _evaluate_period(zip(*eaten_per_day),
                              [g*len(diet) for g in goal],
                              config['NUTRIENTS_WEIGHTS'])
    return daily + variety + period

def calculate_nutrients(diet, food):
    return _calculate_nutrients_from_eaten(_get_eaten_per_day(diet, food))

def _make_move(state, temperature, goal, food, config):
    random_neighbour = _get_random_neighbour(state)
    current_target = target_function(state, goal, food, config)
    next_target = target_function(random_neighbour, goal, food, config)
    delta_target = current_target - next_target
    if delta_target >= 0:
        _PLOT_POINTS.append(next_target)
        return random_neighbour
    acceptance = math.exp(delta_target / temperature)

    if random() < acceptance:
        _PLOT_POINTS.append(next_target)
        return random_neighbour

    _PLOT_POINTS.append(current_target)
    return state

def _get_starting_point(number_of_days, number_of_food): #TODO: Think of a better starting point
    return [[0 for _ in range(number_of_food)] for _ in range(number_of_days)]

def _get_random_params(diet):
    day = randint(0, len(diet) - 1)
    food = randint(0, len(diet[day]) - 1)
    increment = randint(0, 1)
    return day, food, increment

def _get_random_neighbour(diet):
    day, food, increment = _get_random_params(diet)
    while(diet[day][food] == 0 and increment == 0):
        day, food, increment = _get_random_params(diet)
    new_state = deepcopy(diet)
    new_state[day][food] += (1 if increment == 1 else -1)
    return new_state

def _get_neighbours(diet, jump):
    def _add_to_results(results, day_index, index, jump):
        result = deepcopy(diet)
        new = result[day_index][index] + jump
        result[day_index][index] = new if new >= 0 else 0
        results.append(result)

    results = []
    for i, day in enumerate(diet):
        for j, _ in enumerate(day):
            _add_to_results(results, i, j, jump)
            _add_to_results(results, i, j, -jump)
    return results

def _calculate_nutrients_from_eaten(eaten_per_day):
    return [sum(col)
            for col
            in zip(*eaten_per_day)]

def _get_eaten_per_day(diet, foods):
    results = [[0 for _ in range(4)] for _ in enumerate(diet)]
    for day, result in zip(diet, results):
        for amount, food in zip(day, foods.values()):
            for i, _ in enumerate(result):
                result[i] += amount*food[i]
    return results

def _evaluate_period(nutrients_period, goals_period, weight_functions):
    return sum(weight_function(abs(sum(nutrients) - goal_period))
               for nutrients, goal_period, weight_function
               in zip(nutrients_period, goals_period, weight_functions))

def _evaluate_variety(daily_nutrients, weight_function):
    diff_sum = sum(abs(a - b)
                   for a, b in itertools.combinations(daily_nutrients, r=2)
                   if a != 0 and b != 0)
    return weight_function(sum(daily_nutrients) - diff_sum/len(daily_nutrients))

def _evaluate_day(nutrients, daily_goals, weight_functions):
    return sum(weight_function(abs(nutrient - daily_goal))
               for nutrient, daily_goal, weight_function
               in zip(nutrients, daily_goals, weight_functions))

class SimulatedAnnealingTests(unittest.TestCase):
    self_function = staticmethod(lambda x: x)
    square_function = staticmethod(lambda x: x*x)
    negate_function = staticmethod(lambda x: -x)
    halve_function = staticmethod(lambda x: x/2.0)

    @staticmethod
    def is_permutation(left, right):
        count = defaultdict(int)
        for elem in left:
            temp = tuple(tuple(i) for i in elem)
            count[temp] += 1
        for elem in right:
            temp = tuple(tuple(i) for i in elem)
            count[temp] -= 1
        return not any(count.values())

    def test_evaluate_day_1(self):
        day = [3, 5, 6, 12]
        goal = [3, 5, 6, 12]
        functions = Namespace(**{'value' : [self.negate_function]*4})
        evaluated = _evaluate_day(day, goal, functions)
        self.assertEqual(0, evaluated)

    def test_evaluate_day_2(self):
        day = [3, 5, 6, 12]
        goal = [5, 2, 1, 0]
        functions = Namespace(**{'value' : [self.self_function]*4})
        evaluated = _evaluate_day(day, goal, functions)
        self.assertEqual(22, evaluated)

    def test_evaluate_day_3(self):
        day = [3, 5, 6, 12]
        goal = [3, 0, 4, 2]
        functions = Namespace(**{'value' : [self.self_function,
                                            self.square_function,
                                            self.negate_function,
                                            self.halve_function]})
        evaluated = _evaluate_day(day, goal, functions)
        self.assertEqual(28, evaluated)

    def test_evaluate_variety_1(self):
        nutrients = [1, 6, 9]
        evaluated = _evaluate_variety(nutrients, self.self_function)
        self.assertAlmostEqual(10 + 2/3.0, evaluated)

    def test_evaluate_variety_2(self):
        nutrients = [0, 6, 9]
        evaluated = _evaluate_variety(nutrients, self.self_function)
        self.assertAlmostEqual(14.0, evaluated)

    def test_evaluate_variety_3(self):
        nutrients = [0, 6, 3, 2]
        evaluated = _evaluate_variety(nutrients, self.square_function)
        self.assertAlmostEqual(81, evaluated)

    def test_evaluate_variety_4(self):
        nutrients = [4, 1, 3]
        evaluated = _evaluate_variety(nutrients, self.self_function)
        self.assertAlmostEqual(6.0, evaluated)

    def test_evaluate_period_1(self):
        nutrients = [[1, 2, 3], [3, 2, 1], [1, 1, 1], [2, 2, 2]]
        goals = [6, 3, 0, 1]
        functions = Namespace(**{'value' : [self.self_function]*4})
        evaluated = _evaluate_period(nutrients, goals, functions)
        self.assertEqual(11, evaluated)

    def test_evaluate_period_2(self):
        nutrients = [[1, 2, 3], [3, 2, 1], [1, 1, 1], [2, 2, 2]]
        goals = [6, 3, 0, 1]
        functions = Namespace(**{'value' : [self.self_function,
                                            self.square_function,
                                            self.negate_function,
                                            self.halve_function]})
        evaluated = _evaluate_period(nutrients, goals, functions)
        self.assertEqual(8.5, evaluated)

    def test_calculate_nutrients_1(self):
        food = OrderedDict(sorted({'a': [1, 2, 3, 4],
                                   'b': [4, 3, 2, 1]}.items()))
        diet = [[1, 3], [1, 0], [1, 1]]
        expected_nutrients = [19, 18, 17, 16]
        self.assertEqual(expected_nutrients, calculate_nutrients(diet, food))

    def test_calculate_nutrients_2(self):
        food = OrderedDict(sorted({'a': [1, 1, 1, 1],
                                   'b': [0, 1, 0, 2]}.items()))
        diet = [[1, 1], [1, 2]]
        expected_nutrients = [2, 5, 2, 8]
        self.assertEqual(expected_nutrients, calculate_nutrients(diet, food))

    def test_target_function(self):
        goals = [100, 150, 75, 20]
        diet = [[1, 2, 3, 4], [6, 6, 6, 1], [9, 1, 1, 3]]
        food = OrderedDict()
        food.update({'Kimchi' : [10, 15, 20, 1]})
        food.update({'Jajo'   : [20, 5, 10, 2]})
        food.update({'Manna'  : [1, 5, 10, 5]})
        food.update({'Stek'   : [1, 1, 1, 1]})

        function = self.self_function
        config_mock = {
            'NUTRIENTS_WEIGHTS' : [function] * 4,
            'VARIETY_WEIGHT' : function
        }

        result = target_function(diet, goals, food, ConfigMock)
        self.assertEqual(1101, result)

    def test_get_neighbours_1(self):
        diet = [[1, 2], [3, 4]]
        neighbours = [
            [[0, 2], [3, 4]],
            [[2, 2], [3, 4]],
            [[1, 1], [3, 4]],
            [[1, 3], [3, 4]],
            [[1, 2], [2, 4]],
            [[1, 2], [4, 4]],
            [[1, 2], [3, 3]],
            [[1, 2], [3, 5]],
        ]
        self.assertTrue(self.is_permutation(neighbours, _get_neighbours(diet, 1)))

    def test_get_neighbours_2(self):
        diet = [[1, 1, 1]]
        neighbours = [
            [[0, 1, 1]],
            [[3, 1, 1]],
            [[1, 0, 1]],
            [[1, 3, 1]],
            [[1, 1, 0]],
            [[1, 1, 3]],
        ]
        self.assertTrue(self.is_permutation(neighbours, _get_neighbours(diet, 2)))

    def test_get_neighbours_3(self):
        diet = [[5, 5, 5]]
        neighbours = [
            [[2, 5, 5]],
            [[8, 5, 5]],
            [[5, 2, 5]],
            [[5, 8, 5]],
            [[5, 5, 2]],
            [[5, 5, 8]],
        ]
        self.assertTrue(self.is_permutation(neighbours, _get_neighbours(diet, 3)))

if __name__ == '__main__':
    unittest.main()
