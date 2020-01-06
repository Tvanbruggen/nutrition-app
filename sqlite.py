import sqlite3
from sqlite3 import OperationalError, IntegrityError, ProgrammingError
from ingredientList import *
from mealList import *
from dayList import *
import mvc_exceptions as mvc_exc
import numpy as np

DB_name = 'db/DB.db'

sql_create_ingredients_table = """ CREATE TABLE IF NOT EXISTS Ingredients (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT UNIQUE,
                                    kcal REAL,
                                    koolh REAL,
                                    prot REAL,
                                    vet REAL,
                                    vez REAL
                                ); """

sql_create_meals_table = """CREATE TABLE IF NOT EXISTS Meals (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT UNIQUE,
                                    kcal REAL,
                                    koolh REAL,
                                    prot REAL,
                                    vet REAL,
                                    vez REAL
                            );"""

sql_create_days_table = """CREATE TABLE IF NOT EXISTS Days (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        name TEXT UNIQUE,
                                        kcal REAL,
                                        koolh REAL,
                                        prot REAL,
                                        vet REAL,
                                        vez REAL
                                );"""

sql_create_ml_table = """CREATE TABLE IF NOT EXISTS MealsIngredients (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    meal_id INTEGER,
                                    ingredient_id INTEGER,
                                    amount INTEGER
                            );"""

sql_create_dm_table = """CREATE TABLE IF NOT EXISTS DaysMeals (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    day_id INTEGER,
                                    meal_id INTEGER
                            );"""


def connect_to_db(db=None):
    """Connect to a sqlite DB. Create the database if there isn't one yet.


    Open a connection to a SQLite DB (either a DB file or an in-memory DB).
    When a database is accessed by multiple connections, and one of the
    processes modifies the database, the SQLite database is locked until that
    transaction is committed.

    Parameters
    ----------
    db : str
        database name (without .db extension). If None, create an In-Memory DB.

    Returns
    -------
    connection : sqlite3.Connection
        connection object
    """
    if db is None:
        mydb = ':memory:'
        print('New connection to in-memory SQLite DB...')
    else:
        mydb = '{}.db'.format(db)
        print('New connection to SQLite DB...')
    connection = sqlite3.connect(mydb)
    return connection


def connect(func):
    """Decorator to (re)open a sqlite database connection when needed.

    A database connection must be open when we want to perform a database query
    but we are in one of the following situations:
    1) there is no connection
    2) the connection is closed

    Parameters
    ----------
    func : function
        function which performs the database query

    Returns
    -------
    inner func : function
    """
    def inner_func(conn, *args, **kwargs):
        try:
            # I don't know if this is the simplest and fastest query to try
            conn.execute(
                'SELECT name FROM sqlite_temp_master WHERE type="table";')
        except (AttributeError, ProgrammingError):
            conn = connect_to_db(DB_name)
        return func(conn, *args, **kwargs)
    return inner_func


def disconnect_from_db(db=None, conn=None):
    if db is not DB_name:
        print("You are trying to disconnect from a wrong DB")
    if conn is not None:
        conn.close()


@connect
def create_table(conn, create_sql_table):
    try:
        conn.execute(create_sql_table)
    except OperationalError as e:
        print(e)


@connect
def select_one(conn, name, table_name):
    # Create query for obtaining item
    sql = 'SELECT * FROM "{}" WHERE name="{}"'.format(table_name, name)
    c = conn.execute(sql)
    result = c.fetchone()

    # Check if result is not zero
    if result is not None:
        return result
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t read "{}" because it\'s not stored in table "{}"'
            .format(name, table_name))


@connect
def select_ingredient(conn, ingredient_name):
    # Create query for obtaining ingredient
    sql_ingredient = 'SELECT * FROM Ingredients WHERE name="{}"'.format(ingredient_name)
    c = conn.execute(sql_ingredient)
    ingredient_tuple = c.fetchone()

    # Check if result is not zero
    if ingredient_tuple is not None:
        return convert_ingredient(ingredient_tuple)
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t read "{}" because it\'s not stored in table Ingredient'
            .format(ingredient_name))


@connect
def select_ingredients(conn):
    # Create query for obtaining ingredient
    sql = 'SELECT * FROM Ingredients'
    c = conn.execute(sql)
    ingredient_tuples = c.fetchall()

    # Check if result is not zero
    if ingredient_tuples is not None:
        # Convert the tuples to ingredients
        ingredients = list()
        for ingredient_tuple in ingredient_tuples:
            ingredients.append(convert_ingredient(ingredient_tuple))

        return ingredients
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t read, because nothing is stored in table Ingredients')


@connect
def insert_ingredient(conn, ingredient):
    sql = "INSERT OR IGNORE INTO Ingredients ('name', 'kcal', 'koolh', 'prot', 'vet', 'vez') " \
          "VALUES (?, ?, ?, ?, ?, ?)"
    n = ingredient.get_nutr()
    entry = (ingredient.name, n[0], n[1], n[2], n[3], n[4])
    try:
        conn.execute(sql, entry)
        conn.commit()
    except IntegrityError as e:
        raise mvc_exc.ItemAlreadyStored(
            '{}: "{}" already stored in table Ingredients'.format(e, ingredient.name))


@connect
def insert_ingredients(conn, ingredients):
    # Create query for obtaining ingredient
    sql = "INSERT OR IGNORE INTO Ingredients ('name', 'kcal', 'koolh', 'prot', 'vet', 'vez') VALUES (?, ?, ?, ?, ?, ?)"

    # Define list for executing many queries
    entries = list()

    # Convert ingredient list to entry list for the queries
    for i in ingredients:
        n = i.get_nutr()
        entries.append((i.name, n[0], n[1], n[2], n[3], n[4]))
    try:
        conn.executemany(sql, entries)
        conn.commit()
    except IntegrityError as e:
        print('{}: at least one in {} was already stored in table "{}"'
              .format(e, [i.name for i in ingredients], "Ingredients"))


@connect
def insert_meal(conn, meal_name):
    meal = Meal(meal_name)
    if not is_present(conn, meal, "Meals"):
        # Insert meal in database
        sql = "INSERT OR IGNORE INTO Meals ('name', 'kcal', 'koolh', 'prot', 'vet', 'vez') VALUES (?, ?, ?, ?, ?, ?)"
        nutr = meal.get_nutr()
        try:
            conn.execute(sql, (meal.name, nutr[0], nutr[1], nutr[2], nutr[3], nutr[4]))
            conn.commit()
        except IntegrityError as e:
            raise mvc_exc.ItemAlreadyStored(
                '{}: "{}" already stored in table Meals'.format(e, meal.name))

        # # Get meal from database to obtain meal id
        # meal_tuple = select_one(conn, meal.name, "Meals")
        #
        # # Initialize entry list for sql query
        # entries = list()
        #
        # for n, ingredient in enumerate(meal.read_ingredients()):
        #     # Obtain ingredient tuple for the location of the ingredient
        #     ingredient_tuple = select_one(conn, ingredient.name, "Ingredients")
        #
        #     # Store the all entries for the sql query
        #     entries.append((meal_tuple[0], ingredient_tuple[0], meal.amounts[n]))
        #     # i_id.append(ingredient_tuple[0])
        #
        # sql = "INSERT OR IGNORE INTO MealsIngredients ('meal_id', 'ingredient_id', 'amount') VALUES (?, ?, ?)"
        # try:
        #     conn.executemany(sql, entries)
        #     conn.commit()
        # except IntegrityError as e:
        #     print('At least one was already stored in table MealsIngredients')


# TODO
# UPDATE THE MEALSINGREDIENTS ROWS
@connect
def update_meal(conn, meal_name, ingredients, amounts):

    # sql_check = 'SELECT EXISTS(SELECT 1 FROM Meals WHERE name=? LIMIT 1)'
    sql_update = 'UPDATE Meals SET kcal=?, koolh=?, prot=?, vet=?, vez=? WHERE name=?'

    # Check if meal exists
    sql = 'SELECT * FROM Meals WHERE name="{}"'.format(meal_name)
    c = conn.execute(sql)
    meal_tuple = c.fetchone()

    if meal_tuple:

        # Initialize entry list for sql query
        entries = list()
        nutr = np.zeros(5)

        for n, ingredient in enumerate(ingredients):
            # Obtain ingredient tuple for the location of the ingredient
            ingredient_tuple = select_one(conn, ingredient.name, "Ingredients")

            nutr = nutr + np.asarray(ingredient_tuple[2:7])*amounts[n]/100

            # Store the all entries for the sql query
            entries.append((meal_tuple[0], ingredient_tuple[0], amounts[n]))

        sql = "INSERT OR IGNORE INTO MealsIngredients ('meal_id', 'ingredient_id', 'amount') VALUES (?, ?, ?)"
        try:
            conn.executemany(sql, entries)
            conn.commit()
        except IntegrityError as e:
            print('At least one was already stored in table MealsIngredients')

        c.execute(sql_update, (nutr[0], nutr[0], nutr[0], nutr[0], nutr[0], meal_name))
        conn.commit()
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t update "{}" because it\'s not stored in table Meals'.format(meal_name))


@connect
def select_meal(conn, meal_name):
    # Create query for obtaining ingredient
    # sql_meal = 'SELECT * FROM Meals WHERE name="{}"'.format(meal_name)
    # c = conn.execute(sql_meal)
    meal_tuple = select_one(conn, meal_name, "Meals")

    # Check if result is not zero
    if meal_tuple is not None:
        # Create new meal object
        meal = Meal(meal_tuple[1])

        # Create query for obtaining ingredient ids
        sql = 'SELECT * FROM MealsIngredients WHERE meal_id="{}"'.format(meal_tuple[0])
        c = conn.execute(sql)
        mi_tuples = c.fetchall()

        # Check if result is not zero
        if mi_tuples is not None:
            for mi_tuple in mi_tuples:
                sql = 'SELECT * FROM Ingredients WHERE id="{}"'.format(mi_tuple[2])
                c = conn.execute(sql)
                ingredient_tuple = c.fetchone()

                # Check if result is not zero
                if ingredient_tuple is not None:
                    meal.add_ingredient(convert_ingredient(ingredient_tuple), mi_tuple[3])

            return meal
        else:
            raise mvc_exc.ItemNotStored(
                'Can\'t read "{}" because it\'s not stored in table "{}"'
                .format(meal_tuple[0], "IngredientsMeals"))
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t read "{}" because it\'s not stored in table "{}"'
            .format(meal_name, "Meals"))


@connect
def select_meals(conn):
    # Create query for obtaining ingredient
    sql_meal = 'SELECT * FROM Meals'
    c = conn.execute(sql_meal)
    meal_tuples = c.fetchall()

    # Create list to store meals
    meals = list()

    # For all meals append the list of meals
    for meal_tuple in meal_tuples:
        meals.append(select_meal(conn, meal_tuple[1]))

    return meals


@connect
def insert_day(conn, day_name):
    # Create Day object
    day = Day(day_name)
    if not is_present(conn, day, "Days"):
        # Insert day in database
        sql = "INSERT OR IGNORE INTO Days ('name', 'kcal', 'koolh', 'prot', 'vet', 'vez') VALUES (?, ?, ?, ?, ?, ?)"
        nutr = day.get_nutr()
        try:
            conn.execute(sql, (day.name, nutr[0], nutr[1], nutr[2], nutr[3], nutr[4]))
            conn.commit()
        except IntegrityError as e:
            raise mvc_exc.ItemAlreadyStored(
                '{}: "{}" already stored in table Days'.format(e, day.name))

        # # Get day from database to obtain day id
        # day_tuple = select_one(conn, day.name, "Days")
        #
        # # Initialize entry list for sql query
        # entries = list()
        #
        # for n, meal in enumerate(day.read_meals()):
        #     # Obtain meal tuple for the location of the meal
        #     meal_tuple = select_one(conn, meal.name, "Meals")
        #
        #     # Store the all entries for the sql query
        #     entries.append((day_tuple[0], meal_tuple[0]))
        #
        # sql = "INSERT OR IGNORE INTO DaysMeals ('day_id', 'meal_id') VALUES (?, ?)"
        # try:
        #     conn.executemany(sql, entries)
        #     conn.commit()
        # except IntegrityError as e:
        #     print('At least one was already stored in table DaysMeals')


@connect
def select_day(conn, day_name):
    # Create query for obtaining day
    # sql = 'SELECT * FROM Days WHERE name="{}"'.format(day_name)
    # c = conn.execute(sql)
    day_tuple = select_one(conn, day_name, "Days")

    # Check if result is not zero
    if day_tuple is not None:
        # Create new day object
        day = Day(day_tuple[1])

        # Create query for obtaining meals ids
        sql = 'SELECT * FROM DaysMeals WHERE day_id="{}"'.format(day_tuple[0])
        c = conn.execute(sql)
        dm_tuples = c.fetchall()

        # Check if result is not zero
        if dm_tuples is not None:
            for dm_tuple in dm_tuples:
                sql = 'SELECT * FROM Meals WHERE id="{}"'.format(dm_tuple[2])
                c = conn.execute(sql)
                meal_tuples = c.fetchall()

                # Create list for meal objects
                meals = list()

                # Check if result is not zero
                if meal_tuples is not None:
                    for meal_tuple in meal_tuples:
                        meals.append(select_meal(conn, meal_tuple[1]))

                day.add_meals(meals)
        else:
            raise mvc_exc.ItemNotStored(
                'Can\'t read "{}" because it\'s not stored in table DaysMeals'
                .format(day_tuple[0]))
        return day
    else:
        raise mvc_exc.ItemNotStored(
            'Can\'t read "{}" because it\'s not stored in table Days'
            .format(day_name))


@connect
def select_days(conn):
    # Create query for obtaining days
    sql = 'SELECT * FROM Days'
    c = conn.execute(sql)
    results = c.fetchall()

    # Create list to store meals
    return_list = list()

    # For all results append the return_list
    for result in results:
        return_list.append(select_day(conn, result[1]))

    return return_list


def convert_ingredient(ingredient_tuple):
    # Create nutr list
    nutr = []
    for n in range(2, 7):
        nutr.append(ingredient_tuple[n])

    # Return ingredient
    return Ingredient(ingredient_tuple[1], nutr)


def convert_ingredient(ingredient_tuple):
    # Create nutr list
    nutr = []
    for n in range(2, 7):
        nutr.append(ingredient_tuple[n])

    # Return ingredient
    return Ingredient(ingredient_tuple[1], nutr)


@connect
def is_present(conn, item, table_name):
    # Create query for obtaining ingredient
    sql = 'SELECT * FROM "{}" WHERE name="{}"'.format(table_name, item.name)
    c = conn.execute(sql)
    result = c.fetchone()

    # Check if result is not zero
    if result is not None:
        return True
    else:
        return False


def main():

    conn = connect_to_db(DB_name)

    # Create tables
    create_table(conn, sql_create_ingredients_table)
    create_table(conn, sql_create_meals_table)
    create_table(conn, sql_create_days_table)
    create_table(conn, sql_create_ml_table)
    create_table(conn, sql_create_dm_table)

    # Create some ingredient objects
    i1 = Ingredient("gehakt", [100, 100, 100, 100, 100])
    i2 = Ingredient("tomatensaus", [200, 200, 200, 200, 200])
    i3 = Ingredient("pasta", [50, 50, 50, 50, 50])
    i4 = Ingredient("kwark", [100, 100, 100, 100, 100])
    i5 = Ingredient("muesli", [50, 50, 50, 50, 50])

    # Insert one ingredient
    insert_ingredient(conn, i1)

    ingredients = list()
    ingredients.append(i2)
    ingredients.append(i3)
    ingredients.append(i4)
    ingredients.append(i5)

    # Insert many ingredients
    insert_ingredients(conn, ingredients)

    ingredients = select_ingredients(conn)
    for i in ingredients:
        print("* {}".format(i.name))

    # Create a meal and add the ingredients
    meal1 = Meal("Spagetthi")
    meal1.add_ingredient(i1, 100)
    meal1.add_ingredient(i2, 200)
    meal1.add_ingredient(i3, 100)

    meal2 = Meal("Ontbijt")
    meal2.add_ingredient(i4, 250)
    meal2.add_ingredient(i5, 100)

    meal3 = Meal("toetje")
    meal3.add_ingredient(i4, 250)

    insert_meal(conn, meal1)
    insert_meal(conn, meal2)
    insert_meal(conn, meal3)

    print("\n")
    meal = select_meal(conn, "Ontbijt")
    print("* {}".format(meal.name))
    for n, i in enumerate(meal.ingredients):
        print("   - {} ({})".format(i.name, meal.amounts[n]))

    print("\n")
    meals = select_meals(conn)
    for meal in meals:
        print("* {}".format(meal.name))
        for n, i in enumerate(meal.ingredients):
            print("   - {} ({})".format(i.name, meal.amounts[n]))

    # Create a day and add the meals
    day1 = Day("01/01/2020")
    day1.add_meal(meal2)
    day1.add_meal(meal1)
    day1.add_meal(meal3)

    day2 = Day("02/01/2020")
    day2.add_meal(meal2)
    day2.add_meal(meal3)

    insert_day(conn, day1)
    insert_day(conn, day2)

    print("\n")
    day = select_day(conn, "01/01/2020")
    print("* {}".format(day.name))
    for m in day.meals:
        print("   - {}".format(m.name))
        for n, i in enumerate(m.ingredients):
            print("      > {} ({})".format(i.name, m.amounts[n]))

    print("\n")
    days = select_days(conn)
    for day in days:
        print("* {}".format(day.name))
        for m in day.meals:
            print("   - {}".format(m.name))
            for n, i in enumerate(m.ingredients):
                print("      > {} ({})".format(i.name, m.amounts[n]))


if __name__ == "__main__":
    main()