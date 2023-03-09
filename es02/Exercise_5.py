from math import *

class Car:

	def __init__(self, name):
		self.__name = name
		self.__speed = 0
		self.__gear = 1

	def __str__(self):
		return f"Car: {self.getName()}, Gear: {self.getGear()}, Speed: {self.getSpeed()}"

	def getSpeed(self):
		return self.__speed

	def getName(self):
		return self.__name

	def getGear(self):
		return self.__gear

	def setName(self, name):
		pass

	def setSpeed(self, speed):	
		if(speed <= 0):
			self.__speed = 0
			return
		if(speed >= 250):
			self.__speed = 250
			return
		self.__speed = speed
		return

	def gearUp(self):
		if( self.__gear == 6 ):
			raise ValueError("Gear already at maximum level")
		self.__gear = self.__gear + 1

	def gearDown(self):
		if( self.__gear == 1 ):
			raise ValueError("Gear already at minimum level")
		self.__gear = self.__gear - 1