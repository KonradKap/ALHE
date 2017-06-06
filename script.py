#!/bin/python3

from simulated_annealing import simulated_annealing

if __name__ == '__main__':
    best_diet = simulated_annealing(4, {'koks' : [0, 0, 0, 1234],
                                        'wóda' : [100, 0, 0, 0],
                                        'polibuda' : [1, 1, 1, 1]})
    print(best_diet)
