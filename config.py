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
    'MAX_ITERATIONS' : 1000,
}

def generate_nutrient_functions(config, original_fn, goals):
    new_config = deepcopy(config)
    new_config['NEW_NUTRIENTS_WEIGHTS'] = [
        lambda x: original_fn(x) * goals[0]/goal
        for goal in goals
    ]
    return new_config
