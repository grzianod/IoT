from math import *
import random

class Card:

	def __init__(self, suit, value):
		if( suit != "Hearts" and suit != "Diamonds" and suit != "Clubs" and suit != "Spades" ):
			raise ValueError("Suit not available")
		if( value != "A" and value != "2" and value != "3" and value != "4" and value != "5" 
			and value != "6" and value != "7" and value != "8" and value != "9" and value != "10" and value != "J" and value != "K" and value != "Q" ):
			raise ValueError("Value not available")
		self.value = value
		self.suit = suit

	def __str__(self):
		return f"{self.value} of {self.suit}"

class Deck:

	def __init__(self):
		self.cards = [ Card("Spades", "K"), Card("Spades", "Q"), Card("Spades", "J"), Card("Spades", "10"), Card("Spades", "9"), Card("Spades", "8"), Card("Spades", "7"), Card("Spades", "6"), Card("Spades", "5"), Card("Spades", "4"), Card("Spades", "3"), Card("Spades", "2"), Card("Spades", "A"),
			Card("Hearts", "K"), Card("Hearts", "Q"), Card("Hearts", "J"), Card("Hearts", "10"), Card("Hearts", "9"), Card("Hearts", "8"), Card("Hearts", "7"), Card("Hearts", "6"), Card("Hearts", "5"), Card("Hearts", "4"), Card("Hearts", "3"), Card("Hearts", "2"), Card("Hearts", "A"),
			Card("Diamonds", "K"), Card("Diamonds", "Q"), Card("Diamonds", "J"), Card("Diamonds", "10"), Card("Diamonds", "9"), Card("Diamonds", "8"), Card("Diamonds", "7"), Card("Diamonds", "6"), Card("Diamonds", "5"), Card("Diamonds", "4"), Card("Diamonds", "3"), Card("Diamonds", "2"), Card("Diamonds", "A"),
			Card("Clubs", "K"), Card("Clubs", "Q"), Card("Clubs", "J"), Card("Clubs", "10"), Card("Clubs", "9"), Card("Clubs", "8"), Card("Clubs", "7"), Card("Clubs", "6"), Card("Clubs", "5"), Card("Clubs", "4"), Card("Clubs", "3"), Card("Clubs", "2"), Card("Clubs", "A") ]

	def deal(self, n):
		if( n > len(self.cards) ):
			raise ValueError("Not enough cards in the deck")
		c = self.cards[0:n:1]
		del self.cards[0:n:1]
		return c

	def shuffle(self):
		random.shuffle(self.cards)

	def __str__(self):
		return f"Card deck containing {len(self.cards)} cards"
