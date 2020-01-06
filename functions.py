from ingredientList import *
from mealList import *

def is_present(name, list):
	present = False
	idx = -1
	for c, i in enumerate(list):
		if i.name == name:
			present = True
			idx = c
	return present, idx
