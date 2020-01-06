from ingredientList import *
from mealList import *
from dayList import *


class View(object):

	@staticmethod
	def show_ingredients(ingredients):
		for ingredient in ingredients:
			print("* {}".format(ingredient.name))
		print(" ")

	@staticmethod
	def show_ingredient(ingredient):
		print("* {}".format(ingredient.name))
		print("\n")

	@staticmethod
	def show_meals(meals):
		for meal in meals:
			print("* {}".format(meal.name))
			for ingredient in meal.ingredients:
				print("   - {}".format(ingredient.name))

		print("\n")

	@staticmethod
	def show_meal(meal):
		meal.__print__()

	@staticmethod
	def show_days(days):
		for day in days:
			print("* {}".format(day.name))
			for meal in day.meals:
				print("   - {}".format(meal.name))
				for ingredient in meal.ingredients:
					print("      > {}".format(ingredient.name))
		print("\n")



class Controller(object):
	def __init__(self, model_i, model_m, model_d, view):
		self.model_ingredients = model_i
		self.model_meals = model_m
		self.model_days = model_d
		self.view = view

	def show_ingredients(self):
		ingredients = self.model_ingredients.read_ingredients()
		self.view.show_ingredients(ingredients)

	def show_ingredient(self, name):
		ingredient = self.model_ingredients.read_ingredient(name)
		self.view.show_ingredient(ingredient)

	def insert_ingredient(self, name, nutr):
		self.model_ingredients.create_ingredient(name, nutr)

	def update_ingredient(self, name, nutr):
		self.model_ingredients.update_ingredient(name, nutr)

	def delete_ingredient(self, name):
		self.model_ingredients.delete_ingredient(name)

	def show_meals(self):
		meals = self.model_meals.read_meals()
		self.view.show_meals(meals)

	def show_meal(self, name):
		meal = self.model.read_meal(name)
		self.view.show_meal(meal)

	def insert_meal(self, name):
		self.model_meals.create_meal(name)

	def meal_add_ingredient(self, name_meal, name_ingredient):
		ingredient = self.model_ingredients.read_ingredient(name_ingredient)
		self.model_meals.add_ingredient(name_meal, ingredient)

	def meal_add__new_ingredient(self, name_meal, name_ingredient, nutr):
		self.model_ingredients.create_ingredient(name_ingredient, nutr)
		ingredient = self.model_ingredients.read_ingredient(name_ingredient)
		self.model_meals.add_ingredient(name_meal, ingredient)

	def update_meal(self, name, ingredient_names):
		ingredients = []
		for ingredient_name in ingredient_names:
			ingredients.append(self.model_ingredients.read_ingredient(ingredient_name))
		self.model_meals.update_meal(name, ingredients)

	def delete_meal(self, name):
		self.model_meals.delete_meal(name)

	def show_days(self):
		days = self.model_days.read_days()
		self.view.show_days(days)

	def insert_day(self, name):
		self.model_days.create_day(name)

	def day_add_meal(self, name_day, name_meal):
		meal = self.model_meals.read_meal(name_meal)
		self.model_days.add_meal(name_day, meal)

	def update_day(self, name, meal_names):
		meals = []
		for meal_name in meal_names:
			meals.append(self.model_meals.read_meal(meal_name))
		self.model_days.update_day(name, meals)

	def delete_day(self, name):
		self.model_days.delete_day(name)

def main():

	# Create controller object
	c = Controller(IngredientList(), MealList(), DayList(), View())

	# Create some ingredients
	c.insert_ingredient("gehakt", [100, 100, 100, 100, 100])
	c.insert_ingredient("tomatensaus", [200, 200, 200, 200, 200])
	c.insert_ingredient("pasta", [50, 50, 50, 50, 50])
	c.insert_ingredient("kwark", [100, 100, 100, 100, 100])
	c.insert_ingredient("muesli", [50, 50, 50, 50, 50])

	# Create a meal with ingredients
	c.insert_meal("spagetthi")
	c.meal_add_ingredient("spagetthi", "tomatensaus")
	c.meal_add_ingredient("spagetthi", "gehakt")
	c.meal_add_ingredient("spagetthi", "pasta")

	c.insert_meal("ontbijt")
	c.meal_add_ingredient("ontbijt", "kwark")
	c.meal_add_ingredient("ontbijt", "muesli")

	c.insert_meal("toetje")
	c.meal_add__new_ingredient("toetje", "vla", [10, 10, 10, 10, 10])

	c.insert_day("01/01/2020")
	c.day_add_meal("01/01/2020", "ontbijt")
	c.day_add_meal("01/01/2020", "spagetthi")

	c.insert_day("02/01/2020")
	c.day_add_meal("02/01/2020", "ontbijt")
	c.day_add_meal("02/01/2020", "spagetthi")
	c.day_add_meal("02/01/2020", "toetje")

	print("\n inital list of ingredients, meals, and days \n")

	# Show ingredients
	c.show_ingredients()
	c.show_meals()
	c.show_days()

	print("update meal \n")
	c.update_meal("spagetthi", ["kwark", "muesli"])
	c.show_meals()

	print("delete meal \n")
	c.delete_meal("toetje")
	c.show_meals()

	print("delete ingredient \n")
	c.delete_ingredient("muesli")
	c.show_ingredients()

	print("update day \n")
	c.update_day("01/01/2020", ["ontbijt"])
	c.show_days()

	print("delete day \n")
	c.delete_day("01/01/2020")
	c.show_days()


if __name__ == "__main__":
	main()

