from modelSQLite import *
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
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_ingredients(self):
        ingredients = self.model.read_ingredients()
        self.view.show_ingredients(ingredients)

    def show_ingredient(self, name):
        ingredient = self.model.read_ingredient(name)
        self.view.show_ingredient(ingredient)

    def insert_ingredient(self, name, nutr):
        self.model.create_ingredient(Ingredient(name, nutr))

    # def update_ingredient(self, name, nutr):
    #     self.model.update_ingredient(name, nutr)

    # def delete_ingredient(self, name):
    #     self.model.delete_ingredient(name)

    def show_meals(self):
        meals = self.model.read_meals()
        self.view.show_meals(meals)

    def show_meal(self, name):
        meal = self.model.read_meal(name)
        self.view.show_meal(meal)

    def insert_meal(self, meal_name):
        self.model.create_meal(meal_name)

    def update_meal(self, name, ingredient_names, amounts):
        ingredients = []
        for ingredient_name in ingredient_names:
            ingredients.append(self.model.read_ingredient(ingredient_name))
        self.model.update_meal(name, ingredients, amounts)

    def delete_meal(self, name):
        self.model.delete_meal(name)

    def show_days(self):
        days = self.model.read_days()
        self.view.show_days(days)

    def insert_day(self, day_name):
        self.model.create_day(day_name)

    def day_add_meal(self, name_day, name_meal):
        meal = self.model.read_meal(name_meal)
        self.model.add_meal(name_day, meal)

    def update_day(self, name, meal_names):
        meals = []
        for meal_name in meal_names:
            meals.append(self.model.read_meal(meal_name))
        self.model.update_day(name, meals)

    def delete_day(self, name):
        self.model.delete_day(name)


def main():

    # Create controller object
    c = Controller(ModelSQLite(), View())

    # Create some ingredients
    c.insert_ingredient("gehakt", [100, 100, 100, 100, 100])
    c.insert_ingredient("tomatensaus", [200, 200, 200, 200, 200])
    c.insert_ingredient("pasta", [50, 50, 50, 50, 50])
    c.insert_ingredient("kwark", [100, 100, 100, 100, 100])
    c.insert_ingredient("muesli", [50, 50, 50, 50, 50])

    # Create a meal with ingredients
    c.insert_meal("spagetthi")
    c.update_meal("spagetthi", ["gehakt", "tomatensaus", "pasta"], [100, 200, 100])

    c.insert_meal("ontbijt")
    c.update_meal("ontbijt", ["kwark", "muesli"], [250, 100])

    c.insert_meal("toetje")
    c.insert_ingredient("vla", [10, 10, 10, 10, 10])
    c.update_meal("toetje", ["vla"], [150])

    c.show_ingredients()

    c.show_meals()

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

    # print("update meal \n")
    # c.update_meal("spagetthi", ["kwark", "muesli"])
    # c.show_meals()

    # print("delete meal \n")
    # c.delete_meal("toetje")
    # c.show_meals()

    # print("delete ingredient \n")
    # c.delete_ingredient("muesli")
    # c.show_ingredients()

    # print("update day \n")
    # c.update_day("01/01/2020", ["ontbijt"])
    # c.show_days()

    # print("delete day \n")
    # c.delete_day("01/01/2020")
    # c.show_days()


if __name__ == "__main__":
    main()

