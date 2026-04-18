import random
#number 34, 35
lst = [1, 4, 7, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 25, 26, 29, 31, 32, 33, 36, 37, 38, 39, 40, 23, 28]
for i in range(40):
	if i == 33 or i == 34:
		number = [1, 2, 3, 4, 5, 6, 7]
		random.shuffle(number)
		print(i + 1, ". ", number[0], number[1], number[2], sep="")
	else:
		print(i + 1, ". ", random.choice(["A", "Б", "B", "Г"] if i + 1 not in lst else ["A", "Б", "B", "Г", "Д"]), sep="")
