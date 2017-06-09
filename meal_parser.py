from collections import OrderedDict


TABLE_NAME = {'MEAL': 0, 'CALORIES': 1, 'PROTEINS': 2, 'CARBS': 3, 'FATS': 4, 'AMOUNT': 5}

class MealParser(object):

	def __init__(self, meals_file):
		self.file = meals_file
		self.meals_dict = OrderedDict()

	def _split_meal(self, line, given_order, count):
		meal = line.split(';')
		for i in range(count):
			meal[i] = meal[i].rstrip()
		meal = self._in_order(meal, given_order, count)
		return meal[0], meal[1:5]

	def read_meals_from_file(self):

		file = open(self.file, 'r')
		columns = file.readline().split(';')
		given_order = [-1] * 5
		count = len(columns) - 1
		for i in range(count):
			columns[i] = columns[i].rstrip().replace(' ', '').upper()
			given_order[i] = TABLE_NAME[columns[i]]

		for line in file:
			name, values = self._split_meal(line, given_order, count)
			self.meals_dict[name] = values
		file.close()
		return self.meals_dict

	@staticmethod
	def _in_order(meal, given_order, count):
		new_values = [-1] * count
		for index in range(count):
			for i in [i for i, x in enumerate(given_order) if x == index]:
				new_values[index] = meal[i]
		for i in range(1, 5):
			try:
				new_values[i] = float((new_values[i].replace(' ', '')).replace(',', '.'))
			except ValueError:
				raise ValueError('Wrong value. Make sure you use integer.')
		return new_values
#parser = Meal_Parser(file_name)
#print parser.read_meals_from_file()
#parser._in_order([1,2,3,4,5])
