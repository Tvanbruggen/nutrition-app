class Item:

	def __init__(self, nutr):
		self.kcal = nutr[0]
		self.koolh = nutr[1]
		self.prot = nutr[2]
		self.vet = nutr[3]
		self.vez = nutr[4]

	def item_print(self):
		print("KiloCalorien: {}".format(self.kcal))
		print("Koolhydraten: {}".format(self.koolh))
		print("Proteine: {}".format(self.prot))
		print("Vet: {}".format(self.vet))
		print("Vezels: {}".format(self.vez))

	def get_nutr(self):
		nutr = []

		nutr.append(self.kcal)
		nutr.append(self.koolh)
		nutr.append(self.prot)
		nutr.append(self.vet)
		nutr.append(self.vez)

		return nutr

	def set_nutr(self, nutr):
		self.kcal = nutr[0]
		self.koolh = nutr[1]
		self.prot = nutr[2]
		self.vet = nutr[3]
		self.vez = nutr[4]

	def get_kcal(self):
		return self.kcal


def is_present(name, list):
	present = False
	idx = -1
	for c, i in enumerate(list):
		if i.name == name:
			present = True
			idx = c
	return present, idx
