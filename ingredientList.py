from item import *
import numpy as np


class Ingredient(Item):

	def __init__(self, name, nutr=[0, 0, 0, 0, 0]):
		super().__init__(nutr)
		self.name = name

	def __print__(self):
		print("{}: ".format(self.name))
		self.item_print()


class IngredientList():

	def __init__(self):
		self.ingredients = []

	def create_ingredient(self, name, nutr=[0, 0, 0, 0, 0]):
		present, idx = is_present(name, self.ingredients)
		if present:
			print("{} already in list".format(name))
		else:
			ingredient = Ingredient(name, nutr)
			self.ingredients.append(ingredient)

	def add_ingredient(self, ingredient):
		self.ingredients.append(ingredient)

	def add_ingredients(self, ingredients):
		for ingredient in ingredients:
			self.ingredients.append(ingredient)

	def read_ingredient(self, name):
		present, idx = is_present(name, self.ingredients)
		if present:
			return self.ingredients[idx]
		else:
			print("{} not present".format(name))

	def read_ingredients(self):
		return [i for i in self.ingredients]

	def update_ingredient(self, name, nutr):
		present, idx = is_present(name, self.ingredients)
		if present:
			self.ingredients[idx].set_nutr(nutr)
		else:
			print("{} not present".format(name))

	def delete_ingredient(self, name):
		present, idx = is_present(name, self.ingredients)
		if present:
			del self.ingredients[idx]
		else:
			print("{} not present".format(name))

	def __print__(self):
		for i in self.ingredients:
			print("* {}".format(i.name))


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
	# Create some test ingredients
	i1 = Ingredient("gehakt", [100, 100, 100, 100, 100])
	i2 = Ingredient("tomatensaus", [200, 200, 200, 200, 200])
	i3 = Ingredient("pasta", [50, 50, 50, 50, 50])

	# CREATE
	iList = IngredientList()
	iList.add_ingredient(i1)
	iList.add_ingredient(i2)
	iList.add_ingredient(i3)

	# READ
	print("\nREAD all ingredients\n")
	ingredients = iList.read_ingredients()
	for i in ingredients:
		print("* {}".format(i.name))

	print("\nREAD gehakt\n")
	print("* {}".format(iList.read_ingredient("gehakt").name))

	# UPDATE
	print("\nUPDATE gehakt\n")
	iList.update_ingredient("gehakt", [50, 50, 50, 50, 50])
	ingredients = iList.read_ingredients()
	for i in ingredients:
		print("* {}".format(i.name))

	# DELETE
	print("\nDELETE gehakt\n")
	iList.delete_ingredient("gehakt")
	ingredients = iList.read_ingredients()
	for i in ingredients:
		print("* {}".format(i.name))


if  __name__ == "__main__":
	main()


