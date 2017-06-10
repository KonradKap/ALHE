import math
import inspect
from copy import deepcopy

_LAMBDA = lambda x: x

FILE_NAME = 'resources/csv.csv'

CONFIG = {
    'NUTRIENTS_WEIGHTS' : [
        _LAMBDA,
        _LAMBDA,
        _LAMBDA,
        _LAMBDA,
    ],
    'VARIETY_WEIGHT' : _LAMBDA,
    'MAX_ITERATIONS' : 20000,
    'TEMPERATURE' : 10,
    'COOLING' : 0.5
}

def generate_nutrient_functions(config, original_fn, goals):
    new_config = deepcopy(config)
    new_config['NEW_NUTRIENTS_WEIGHTS'] = [
        lambda x: original_fn(x) * goals[0]/goal
        for goal in goals
    ]
    return new_config

def get_plot_name(config):
    source = inspect.getsource(config['VARIETY_WEIGHT'])
    return 'plots/c{}_{}_{}_{}.png'.format(
            source[source.find('lambda x:')+10:-1],
            config['MAX_ITERATIONS'],
            config['TEMPERATURE'],
            config['COOLING']
    )

def generate_cooling_rate(config):
    config['COOLING'] = (1.0/config['TEMPERATURE'])**(1.0/config['MAX_ITERATIONS'])

