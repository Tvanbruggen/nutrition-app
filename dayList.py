from mealList import *
import numpy as np


class Day(Item):

	def __init__(self, name, nutr=[0,0,0,0,0]):
		super().__init__(nutr)
		self.name = name
		self.meals = []

	def add_meal(self, meal):
		present, idx = is_present(meal.name, self.meals)
		if present:
			print("{} already in the list".format(meal.name))
		else:
			self.meals.append(meal)
			self.update_total()

	def add_meals(self, meals):
		for meal in meals:
			self.add_meal(meal)

	def read_meal(self, name):
		present, idx = is_present(name, self.meals)
		if present:
			return self.meals[idx]
		else:
			print("{} not in the list".format(name))

	def read_meals(self):
		return [meal for meal in self.meals]

	def update_day(self, meals):
		self.meals = meals

	def delete_meal(self, name):
		present, idx = is_present(name, self.meals)
		if present:
			del self.ingredient[idx]
			self.update_total()
		else:
			print("{} not in the list".format(name))

	def update_total(self):
		total = np.zeros(5)
		for meal in self.meals:
			nutr = meal.get_nutr()
			total = total + nutr
		self.set_nutr(total)

	def __print__(self):
		print("{}: ".format(self.name))
		meals = []
		for meal in self.meals:
			ingr.append(meal.name)
		print(meal)
		self.item_print()


class DayList():

	def __init__(self):
		self.days = []

	def create_day(self, name, nutr = [0,0,0,0,0]):
		present, idx = is_present(name, self.days)
		if present:
			print("{} already in meal list".format(name))
		else:
			day = Day(name, nutr)
			self.days.append(day)

	def add_day(self, day):
		self.days.append(day)

	def add_meal(self, name, meal):
		day = self.read_day(name)
		day.add_meal(meal)

	def read_day(self, name):
		present, idx = is_present(name, self.days)
		if present:
			return self.days[idx]
		else:
			print("{} not in the list".format(name))

	def read_days(self):
		return [day for day in self.days]

	def update_day(self, name, meals):
		day = self.read_day(name)
		day.update_day(meals)

	def delete_day(self, name):
		present, idx = is_present(name, self.days)
		if present:
			del self.days[idx]
		else:
			print("{} not in the list".format(name))

	def delete_all(self):
		self.days = []

	def __print__(self):
		print("{}: ".format(self.name))
		d = []
		for day in self.days:
			d.append(day.name)
		print(d)
		self.item_print()


def is_present(name, list):
	present = False
	idx = -1
	for c, i in enumerate(list):
		if i.name == name:
			present = True
			idx = c
			return present, idx
	return present, idx


def main():
	# Create some ingredients
	i1 = Ingredient("gehakt", [100, 100, 100, 100, 100])
	i2 = Ingredient("tomatensaus", [200, 200, 200, 200, 200])
	i3 = Ingredient("pasta", [50, 50, 50, 50, 50])

	# Create a meal and add the ingredients
	meal1 = Meal("Spagetthi")
	meal1.add_ingredient(i1, 100)
	meal1.add_ingredient(i2, 200)
	meal1.add_ingredient(i3, 100)

	# Create some more ingredients
	i4 = Ingredient("kwark", [100, 100, 100, 100, 100])
	i5 = Ingredient("muesli", [50, 50, 50, 50, 50])

	# Create a second meal and add the other ingredients
	meal2 = Meal("Ontbijt")
	meal2.add_ingredient(i4, 250)
	meal2.add_ingredient(i5, 100)

	# Create a third meal
	meal3 = Meal("Toetje")	

	# CREATE
	day1 = Day("01/01/2020")
	day1.add_meal(meal1)
	day1.add_meal(meal2)
	day1.add_meal(meal3)

	day2 = Day("02/01/2020")
	day2.add_meal(meal2)
	day2.add_meal(meal3)

	dList = DayList()
	dList.add_day(day1)
	dList.add_day(day2)

	# READ
	print("\nREAD DAY\n")
	days = dList.read_days()
	for day in days:
		print("* {}".format(day.name))
		for m in day.meals:
			print("   - {}".format(m.name))
			for n, i in enumerate(m.ingredients):
				print("      > {} ({})".format(i.name, m.amounts[n]))

	print("\nREAD 01/01/2020\n")
	day = dList.read_day("01/01/2020")
	print("* {}".format(day.name))

	# DELETE
	print("\nDELETE 01/01/2020\n")
	dList.delete_day("01/01/2020")
	days = dList.read_days()
	for day in days:
		print("* {}".format(day.name))
		for m in day.meals:
			print("   - {}".format(m.name))
			for n, i in enumerate(m.ingredients):
				print("      > {} ({})".format(i.name, m.amounts[n]))

	print("\nDELETE ALL\n")
	dList.delete_all()
	days = dList.read_days()
	for day in days:
		print("* {}".format(day.name))
		for m in day.meals:
			print("   - {}".format(m.name))
			for n, i in enumerate(m.ingredients):
				print("      > {} ({})".format(i.name, m.amounts[n]))


if __name__ == "__main__":
	main()

