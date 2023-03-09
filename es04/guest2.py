from guest import Guest
import random
import string
import time

if __name__ == "__main__":
	guest2 = Guest("PLUTO")

	while True:
		n = random.randint(0,20)
		string = ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for i in range(n+1))
		guest2.send(string)
		time.sleep(n)

