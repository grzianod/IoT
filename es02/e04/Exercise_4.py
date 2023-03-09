from math import *

class Circle:

	def __init__(self, radius: float):
		self.radius = radius

	def surface(self):
		return 3.14 * (self.radius**2)

	def perimeter(self):
		return 2 * 3.14 * self.radius

	def __str__(self):
		return f"A circle of radius {self.radius}"

class Cylinder(Circle):

	def __init__(self, radius, height):
		self.circle = Circle(radius)
		self.height = height

	def surface(self):
		return self.height * self.circle.perimeter() + 2 * self.circle.surface()

	def volume(self):
		return self.height * self.circle.surface()

	def __str__(self):
		return f"A cylinder of radius {self.circle.radius} and height {self.height}"