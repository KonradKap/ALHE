from enum import Enum

_LAMBDA = lambda x: x

FILE_NAME = 'resources/csv.csv'

class Config(Enum):
    NUTRIENTS_WEIGHTS = [
        _LAMBDA,
        _LAMBDA,
        _LAMBDA,
        _LAMBDA,
    ]
    VARIETY_WEIGHT = _LAMBDA
    MAX_ITERATIONS = 1000
