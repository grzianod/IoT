def sum(a,b):
	return a+b
def sub(a,b):
	return a-b
def mul(a,b):
	return a*b
def div(a,b):
	return a/b

if __name__ == "__main__":
	a = (int)(input("Insert a: "))
	b = (int)(input("Insert b: "))

	print(f"SUM: {sum(a,b)}")
	print(f"SUB: {sub(a,b)}")
	print(f"MUL: {mul(a,b)}")
	print(f"DIV: {div(a,b)}")