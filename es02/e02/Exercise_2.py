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

class Line:
	"this is class Line to manage all possible operation on a Line"

	def __init__(self, m:int, q:int):
		self.m = m
		self.q = q

	def line_from_points(self, a:Point, b:Point):
		m = (b.y-a.y)/(b.x-a.x)
		self.m = m
		self.q =  (a.y - m * a.x)

	def __str__(self):
		return f"Line: y = {self.m}x + {self.q}"

	def distance(self, a:Point):
		return abs(a.y-self.m*a.x-self.q)/sqrt(1+self.m**2)

	def intersection(self, line):
		if(self.m == self.q):
			return "the lines have no intersection"
		x = (line.q - self.q)/(self.m - line.m)
		return Point( x, self.m * x + self.q)
