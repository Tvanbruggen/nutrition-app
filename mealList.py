from ingredientList import *
import numpy as np


class Meal(Item):

	def __init__(self, name, nutr=[0, 0, 0, 0, 0]):
		super().__init__(nutr)
		self.name = name
		self.ingredients = []
		self.amounts = []

	def add_ingredient(self, ingredient, amount):
		present, idx = is_present(ingredient.name, self.ingredients)
		if present:
			print("{} already in meal".format(ingredient.name))
		else:
			self.ingredients.append(ingredient)
			self.amounts.append(amount)
			self.update_total()

	def add_ingredients(self, ingredients, amounts):
		for n, ingredient in enumerate(ingredients):
			self.add_ingredient(ingredient, amounts[n])

	def read_ingredients(self):
		return self.ingredients

	def read_amounts(self):
		return self.amounts

	def update_ingredients(self, ingredients, amounts):
		self.ingredients = ingredients
		self.amounts = amounts

	def del_ingredient(self, name):
		present, idx = is_present(name, self.ingredients)
		if present:
			del self.ingredient[idx]
			del self.amounts[idx]
			self.update_total()

	def update_total(self):
		total = np.zeros(5)
		for n, ingredient in enumerate(self.ingredients):
			nutr = np.asarray(ingredient.get_nutr())
			amount = self.amounts[n]
			total = total + nutr * amount/100
		self.set_nutr(total)

	def __print__(self):
		print("{}: ".format(self.name))
		ingr = []
		for ingredient in self.ingredients:
			ingr.append(ingredient.name)
		print(ingr)
		self.item_print()


class MealList():

	def __init__(self):
		self.meals = []

	def create_meal(self, name):
		present, idx = is_present(name, self.meals)
		if present:
			print("{} already in meal list".format(name))
		else:
			meal = Meal(name)
			self.meals.append(meal)

	def add_meal(self, meal):
		self.meals.append(meal)

	def read_meal(self, name):
		present, idx = is_present(name, self.meals)
		if present:
			return self.meals[idx]
		else:
			print("{} not in the list".format(name))

	def read_meals(self):
		return [name for name in self.meals]

	def add_ingredient(self, name, ingredient, amount):
		meal = self.read_meal(name)
		meal.add_ingredient(ingredient, amount)

	def update_meal(self, name, ingredients, amounts):
		meal = self.read_meal(name)
		meal.update_ingredients(ingredients, amounts)

	def delete_meal(self, name):
		present, idx = is_present(name, self.meals)
		if present:
			del self.meals[idx]
		else:
			print("{} not in the list".format(name))

	def delete_all(self):
		self.meals = []

	def __print__(self):
		print("{}: ".format(self.date))
		m = []
		for meal in self.meals:
			m.append(meal.name)
		print(m)
		self.item_print()


def is_present(name, meal_list):
	present = False
	idx = -1
	for c, i in enumerate(meal_list):
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
	i4 = Ingredient("kwark", [100, 100, 100, 100, 100])
	i5 = Ingredient("muesli", [50, 50, 50, 50, 50])

	# CREATE
	mList = MealList()

	mList.create_meal("Spagetthi")
	mList.add_ingredient("Spagetthi", i1, 100)
	mList.add_ingredient("Spagetthi", i2, 200)
	mList.add_ingredient("Spagetthi", i3, 100)

	mList.create_meal("Ontbijt")
	mList.add_ingredient("Ontbijt", i4, 250)
	mList.add_ingredient("Ontbijt", i5, 100)

	# READ

	print("\nREAD MEALS\n")
	meals = mList.read_meals()
	for meal in meals:
		print("* {}".format(meal.name))
		for n, i in enumerate(meal.ingredients):
			print("   - {} ({})".format(i.name, meal.amounts[n]))

	print("\nREAD ONTBIJT\n")
	meal = mList.read_meal("Ontbijt")
	print("* {}".format(meal.name))
	for n, i in enumerate(meal.ingredients):
		print("   - {} ({})".format(i.name, meal.amounts[n]))

	# DELETE
	print("\nDELETE ONTBIJT\n")
	mList.delete_meal("Ontbijt")
	meals = mList.read_meals()
	for meal in meals:
		print("* {}".format(meal.name))
		for n, i in enumerate(meal.ingredients):
			print("   - {} ({})".format(i.name, meal.amounts[n]))

	print("\nDELETE ALL\n")
	mList.delete_all()
	meals = mList.read_meals()
	for meal in meals:
		print("* {}".format(meal.name))
		for n, i in enumerate(meal.ingredients):
			print("   - {} ({})".format(i.name, meal.amounts[n]))



if __name__ == "__main__":
	main()

