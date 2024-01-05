import random

class Card:
	def __init__(self, rank: int, name: str, suit: str, abbreviation: str):
		self.rank = rank
		self.name = name
		self.suit = suit
		self.abbreviation = abbreviation

class Deck:
	def __init__(self, num_decks=1):
		self.deck = []
		self.discard = []
		self.burned_cards = []
		for i in range(0, num_decks):
			for rank in range(1, 14):
				for suit in ['Spade', 'Heart', 'Diamond', 'Club']:
					suffix = suit[0]
					if rank == 1:
						name = 'Ace'
						abbreviation = f"A{suffix}"
					elif rank == 11:
						name = 'Jack'
						abbreviation = f"J{suffix}"
					elif rank == 12:
						name = 'Queen'
						abbreviation = f"Q{suffix}"
					elif rank == 13:
						name == 'King'
						abbreviation = f"K{suffix}"
					else:
						name = f"{rank}"
						abbreviation = f"{rank}{suffix}"
					self.deck.append(
						Card(
							int(rank),
							name,
							suit,
							abbreviation
						)
					)

	def __str__(self):
		deck_string = f'[{self.deck[0].abbreviation}'
		for card in self.deck[1:]:
			deck_string = f"{deck_string}, {card.abbreviation}"

		return deck_string + ']'

	def is_empty(self):
		return self.deck == []

	def remaining(self):
		return len(self.deck)

	def shuffle(self):
		for card in self.discard:
			self.deck.append(card)
		for card in self.burned_cards:
			self.deck.append(card)

		random.shuffle(self.deck)

	def draw(self):
		return self.deck.pop()

	def burn(self):
		burn_card = self.deck.pop()
		burn_ammount = burn_card.rank
		# print(f"Burn card was {burn_card.abbreviation}.\n"\
		# 	  f"Burning {burn_ammount} cards")

		self.burned_cards.append(burn_card)
		for i in range(0, burn_ammount):
			burning = self.deck.pop()
			self.discard.append(burning)
			self.burned_cards.append(burning)