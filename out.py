import csv
FORMAT = ['CALORIES', 'PROTEINS', 'CARBS', 'FATS']

def out(food_dict, days, eaten_nutrients, target_function, config):
	filename = '{}.csv'.format(config['FILE_WITH_DIET'])
	with open(filename, 'w', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(['FUNKCJA CELU', target_function])
		spamwriter.writerow(['CEL'])
		spamwriter.writerow(FORMAT)
		spamwriter.writerow(config['GOAL'])
		spamwriter.writerow(['SPOZYTE'])
		spamwriter.writerow(FORMAT)
		spamwriter.writerow(eaten_nutrients)

		calories = []
		proteins = []
		carbs = []
		fats = []
		nutrients = [ calories, proteins, carbs, fats]
		for name, table in zip(FORMAT, nutrients):
			table.append(name)

		column_names = []
		meals = []
		count = 0
		column_names.append('POSILEK')

		for day in days:
			column_names.append('DZIEN {0}'.format(count + 1))
			result = _get_eaten_in_day(day, food_dict)
			for i, component in zip(range(4), nutrients):
				component.append(result[i])

			count += 1

		count = 0
		for meal in food_dict:
			meal_quantity = []
			meal_quantity.append(meal)
			for day in days:
				meal_quantity.append(day[count])
			meals.append(meal_quantity)
			count += 1

		spamwriter.writerow(column_names)
		for meal_quantity in meals:
			spamwriter.writerow(meal_quantity)
		for component in nutrients:
			spamwriter.writerow(component)

def _get_eaten_in_day(day, food_dict):
	result = [0]*4
	for amount, food in zip(day, food_dict.values()):
		for i in range(4):
			result[i] += amount*food[i]
	return result
