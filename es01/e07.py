if __name__ == "__main__":
	a = []
	n = (int)(input("Insert the number of list items: "))
	i=0
	while i<n:
		a.append((int)(input(f"Insert a[{i}]: ")))
		i+=1

	#min
	min = 10000
	max = -10000
	sum = 0
	for item in a:
		if item < min:
			min = item
		if item > max:
			max = item
		sum += item

	print(f"Min: {min}")
	print(f"Max: {max}")
	print(f"Avg: {sum/len(a)}")
