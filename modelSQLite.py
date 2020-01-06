import sqlite
import mvc_exceptions as mvc_exc


class ModelSQLite(object):

    def __init__(self):
        self._connection = sqlite.connect_to_db(sqlite.DB_name)

        # Create tables
        sqlite.create_table(self._connection, sqlite.sql_create_ingredients_table)
        sqlite.create_table(self._connection, sqlite.sql_create_meals_table)
        sqlite.create_table(self._connection, sqlite.sql_create_days_table)
        sqlite.create_table(self._connection, sqlite.sql_create_ml_table)
        sqlite.create_table(self._connection, sqlite.sql_create_dm_table)

    @property
    def connection(self):
        return self._connection

    def create_ingredient(self, ingredient):
        sqlite.insert_ingredient(self.connection, ingredient)

    def create_ingredients(self, ingredients):
        sqlite.insert_ingredients(self.connection, ingredients)

    def create_meal(self, meal_name):
        sqlite.insert_meal(self.connection, meal_name)

    def create_day(self, day_name):
        sqlite.insert_day(self.connection, day_name)

    def read_ingredient(self, ingredient_name):
        return sqlite.select_ingredient(self._connection, ingredient_name)

    def read_ingredients(self):
        return sqlite.select_ingredients(self._connection)

    def read_meal(self, meal_name):
        return sqlite.select_meal(self._connection, meal_name)

    def read_meals(self):
        return sqlite.select_meals(self._connection)

    def read_day(self, day_name):
        return sqlite.select_day(self._connection, day_name)

    def read_days(self):
        return sqlite.select_days(self._connection)

    def update_meal(self, meal_name, ingredients, amounts):
        # ingredients = list()
        # for ingredient_name in ingredient_names:
        #     ingredients.append(self.read_ingredient(ingredient_name))
        sqlite.update_meal(self._connection, meal_name, ingredients, amounts)