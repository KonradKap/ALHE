import itertools
import unittest
from argparse import Namespace
from collections import OrderedDict

from config import Config

def simulated_annealing(number_of_days, food, config):
    pass

def _target_function(diet, goal, food, config):
    eaten_per_day = _get_eaten_per_day(diet, food)
    nutrients = _calculate_nutrients_from_eaten(eaten_per_day)
    daily = sum(_evaluate_day(day, goal, config.nutrients_weights) for day in eaten_per_day)
    variety = sum(_evaluate_variety(day, config.variety_weight) for day in zip(*diet))
    period = _evaluate_period(eaten_per_day,
            [g*len(diet) for g in goal],
            config.nutrients_weights)
    return daily + variety + period

def _calculate_nutrients(diet, food):
    return _calculate_nutrients_from_eaten(_get_eaten_per_day(diet, food))

def _calculate_nutrients_from_eaten(eaten_per_day):
    return [sum(col)
            for col
            in zip(*eaten_per_day)]

def _get_eaten_per_day(diet, foods):
    results = [[0 for i in range(4)] for y in range(len(diet))]
    for day, result in zip(diet, results):
        for amount, food in zip(day, foods.values()):
            for i in range(len(result)):
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
    return weight_function(sum(daily_nutrients) - diff_sum)

def _evaluate_day(nutrients, daily_goals, weight_functions):
    return sum(weight_function(abs(nutrient - daily_goal))
               for nutrient, daily_goal, weight_function
               in zip(nutrients, daily_goals, weight_functions))

class SimulatedAnnealingTests(unittest.TestCase):
    self_function = staticmethod(lambda x: x)
    square_function = staticmethod(lambda x: x*x)
    negate_function = staticmethod(lambda x: -x)
    halve_function = staticmethod(lambda x: x/2.0)

    def test_evaluate_day_1(self):
        day = [3, 5, 6, 12]
        goal = [3, 5, 6, 12]
        functions = [self.negate_function]*4
        evaluated = _evaluate_day(day, goal, functions)
        self.assertEqual(0, evaluated)

    def test_evaluate_day_2(self):
        day = [3, 5, 6, 12]
        goal = [5, 2, 1, 0]
        functions = [self.self_function]*4
        evaluated = _evaluate_day(day, goal, functions)
        self.assertEqual(22, evaluated)

    def test_evaluate_day_3(self):
        day = [3, 5, 6, 12]
        goal = [3, 0, 4, 2]
        functions = [self.self_function,
                     self.square_function,
                     self.negate_function,
                     self.halve_function]
        evaluated = _evaluate_day(day, goal, functions)
        self.assertEqual(28, evaluated)

    def test_evaluate_variety_1(self):
        nutrients = [1, 6, 9]
        evaluated = _evaluate_variety(nutrients, self.self_function)
        self.assertEqual(0, evaluated)

    def test_evaluate_variety_2(self):
        nutrients = [0, 6, 9]
        evaluated = _evaluate_variety(nutrients, self.self_function)
        self.assertEqual(12, evaluated)

    def test_evaluate_variety_3(self):
        nutrients = [0, 6, 3, 2]
        evaluated = _evaluate_variety(nutrients, self.square_function)
        self.assertEqual(9, evaluated)

    def test_evaluate_variety_4(self):
        nutrients = [4, 1, 3]
        evaluated = _evaluate_variety(nutrients, self.self_function)
        self.assertEqual(2, evaluated)

    def test_evaluate_period_1(self):
        nutrients = [[1, 2, 3], [3, 2, 1], [1, 1, 1], [2, 2, 2]]
        goals = [6, 3, 0, 1]
        functions = [self.self_function]*4
        evaluated = _evaluate_period(nutrients, goals, functions)
        self.assertEqual(11, evaluated)

    def test_evaluate_period_2(self):
        nutrients = [[1, 2, 3], [3, 2, 1], [1, 1, 1], [2, 2, 2]]
        goals = [6, 3, 0, 1]
        functions = [self.self_function,
                     self.square_function,
                     self.negate_function,
                     self.halve_function]
        evaluated = _evaluate_period(nutrients, goals, functions)
        self.assertEqual(8.5, evaluated)

    def test_calculate_nutrients_1(self):
        food = OrderedDict(sorted({'a': [1, 2, 3, 4],
                                   'b': [4, 3, 2, 1]}.items()))
        diet = [[1, 3], [1, 0], [1, 1]]
        expected_nutrients = [19, 18, 17, 16]
        self.assertEqual(expected_nutrients, _calculate_nutrients(diet, food))

    def test_calculate_nutrients_2(self):
        food = OrderedDict(sorted({'a': [1, 1, 1, 1],
                                   'b': [0, 1, 0, 2]}.items()))
        diet = [[1, 1], [1, 2]]
        expected_nutrients = [2, 5, 2, 8]
        self.assertEqual(expected_nutrients, _calculate_nutrients(diet, food))

    def test_target_function(self):
        goals = [100, 150, 75, 20]
        diet = [[1, 2, 3, 4], [6, 6, 6, 1], [9, 1, 1, 3]]
        food = OrderedDict(sorted({'Kimchi' : [10, 15, 20, 1],
                                   'Jajo'   : [20, 5, 10, 2],
                                   'Manna'  : [1, 5, 10, 5],
                                   'Stek'   : [1, 1, 1, 1]}.items()))
        config = Namespace(**{'nutrients_weights' : [self.self_function]*4,
                              'variety_weight' : self.self_function})
        result = _target_function(diet, goals, food, config)
        self.assertEqual(1071, result)

if __name__ == '__main__':
    unittest.main()
