if __name__ == "__main__":
	fR = open('original.txt')
	fW = open('copy.txt','w')

	print("The content of the original file is: ", file = fW)
	for line in fR.readlines():
		fW.write(line);

	fR.close();
	fW.close();
