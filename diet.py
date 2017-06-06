class Diet(object):
    def __init__(self, number_of_days, food_size):
        self.solution = [[0] * food_size] * number_of_days

    def __str__(self):
        return str(self.solution)
