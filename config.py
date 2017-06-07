from enum import Enum

class Config(Enum):
    nutrients_weights = [
        staticmethod(lambda x: x),
        staticmethod(lambda x: x),
        staticmethod(lambda x: x),
        staticmethod(lambda x: x)
    ]
    variety_weight = staticmethod(lambda x: x)
