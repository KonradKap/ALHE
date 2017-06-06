import itertools
import unittest

from diet import Diet
from config import Config

def simulated_annealing(number_of_days, food, config):
    return Diet(number_of_days, len(food))

def _target_function(diet, goal, food, config):
    return -1

def _calculate_nutrients(diet, food):
    return [sum(col)
            for col
            in zip(*[
                [nutrient * eaten for nutrient in nutrients]
                for eaten, nutrients
                in [(eaten, nutrient)
                    for day in diet
                    for eaten, nutrient
                    in zip(day, food.values())]])]

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
        self.assertEquals(22, evaluated)

    def test_evaluate_day_3(self):
        day = [3, 5, 6, 12]
        goal = [3, 0, 4, 2]
        functions = [self.self_function,
                     self.square_function,
                     self.negate_function,
                     self.halve_function]
        evaluated = _evaluate_day(day, goal, functions)
        self.assertEquals(28, evaluated)

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
        food = {'a': [1, 2, 3, 4],
                'b': [4, 3, 2, 1]}
        diet = [[1, 3], [1, 0], [1, 1]]
        expected_nutrients = [19, 18, 17, 16]
        self.assertEqual(expected_nutrients, _calculate_nutrients(diet, food))

    def test_calculate_nutrients_2(self):
        food = {'a': [1, 1, 1, 1],
                'b': [0, 1, 0, 1]}
        diet = [[1, 1], [1, 1]]
        expected_nutrients = [2, 4, 2, 4]
        self.assertEqual(expected_nutrients, _calculate_nutrients(diet, food))

    def test_target_function(self):
        goals = [100, 150, 75, 20]


if __name__ == '__main__':
    unittest.main()
