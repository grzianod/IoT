from math import *

class Point:
	"this is class Point to manage all possible operation on a 2D Point"

	def __init__(self, x:int, y:int):
		self.x = x
		self.y = y

	def distance(self, b):
		return sqrt( (self.x-b.x)**2 + (self.y-b.y)**2 )

	def move(self, dx, dy):
		self.x += dx
		self.y += dy

	def __str__(self):
		return f"{self.x},{self.y}"