from math import *

class SquareManager:
	"this is the class SquareManager to manage all possible square operations"

	def __init__(self, side):
		self.side = side

	def area(self):
		return self.side**2

	def perimeter(self):
		return self.side*4

	def diagonal(self):
		return sqrt(2)*self.side