from guest import Guest
import random
import string
import time

if __name__ == "__main__":
	guest1 = Guest("PIPPO")

	while True:
		n = random.randint(0,20)
		string = ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for i in range(n+1))
		guest1.send(string)
		time.sleep(n)

