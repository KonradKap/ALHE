import math
import inspect
from copy import deepcopy

_LAMBDA = lambda x: x

CONFIG = {
    'NUTRIENTS_WEIGHTS' : [
        _LAMBDA,
        _LAMBDA,
        _LAMBDA,
        _LAMBDA,
    ],
    'VARIETY_WEIGHT' : _LAMBDA,
    'MAX_ITERATIONS' : 2000,
    'TEMPERATURE' : 10e5,
    'FILE_NAME' : 'resources/csv.csv',
    'DAYS_OF_DIET' : 10,
    'GOAL' : [2500, 60, 340, 80],
    'FILE_WITH_DIET' : 'resources/diet'
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
    return 'plots/g{}_{}_{}.png'.format(
            source[source.find('lambda x:')+10:-1],
            config['MAX_ITERATIONS'],
            config['TEMPERATURE']
    )
