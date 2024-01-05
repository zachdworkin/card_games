import card
import os

class Payout:
	def __init__(self):
		self.player_wins = 0
		self.banker_wins = 0
		self.ties = 0
		self.banker_half_payout = 0
		self.total_games = 0
		self.banker_only = 0
		self.player_only = 0
		self.banker_only_payout = 0
		self.banker_only_half_payout = 0
		self.player_only_payout = 0
		self.shoe = 0

	def banker_win_percent(self):
		return f"{(self.banker_wins / self.total_games) * 100:.02f}"

	def player_win_percent(self):
		return f"{(self.player_wins / self.total_games) * 100:.02f}"

	def halved_win_percent(self):
		return f"{(self.banker_half_payout / self.total_games) * 100:.02f}"

	def tied_percent(self):
		return f"{(self.ties / self.total_games) * 100:.02f}"

	def banker_only_percent(self):
		return f"{((self.banker_wins + self.banker_half_payout) / self.total_games) * 100:.02f}"

	def player_only_percent(self):
		return f"{((self.player_wins) / self.total_games) * 100:.02f}"

class Player:
	def __init__(self, name: str):
		self.hand = []
		self.name = name
		self.total = 0
		self.score = 0

	def __str__(self):
		return self.name

	def get_hand(self):
		return [card.abbreviation for card in self.hand]

class BaccaratGame:
	def __init__(self, num_decks, verbose=True):
		self.verbose = verbose
		self.num_decks = num_decks
		self.deck = card.Deck(self.num_decks)
		self.players = {
			'player'	: Player("Player"),
			'banker'	: Player("Banker")
		}
		self.tracker = Payout()
		if self.verbose:
			print(f"Created a game with {len(self.players)} players")

	def setup_game(self):
		self.deck = card.Deck(self.num_decks)
		self.tracker.shoe += 1
		self.tracker.player_only_payout = 0
		self.tracker.banker_only_payout = 0
		self.tracker.banker_only_half_payout = 0
		if self.verbose:
			os.system('clear')
			print(f"Setting up game with the {self.tracker.shoe} shoe...")
			print("Shuffling...")

		self.deck.shuffle()
		if self.verbose:
			print("All shuffled")
			print("Burning cards...")

		self.deck.burn()

	def baccarat(self):
		"""
			The main baccarat game sequence.
			Two cards are dealt to each player and banker.
			If either player is dealt a total of an 8 or a 9, both the player
			and banker stand.
			If the player's total is five or less, then the player will receive
			another card. Otherwise the player will stand.
			If the player stands, then the banker hits on a total of 5 or less
			The final betting option, a tie, palys out 8-to-1.
		"""
		if self.verbose:
			print("Dealing...")
		self.deal()

		for player in self.players:
			self.players[player].total = self.sum_hand(self.players[player].hand)

		winner, score, payout = self.play()
		if winner:
			self.players[winner].score += score
		"""
		Round End
		Discard cards when round ends
		"""
		for player in self.players:
			self.players[player].total = 0
			while self.players[player].hand != []:
				c = self.players[player].hand.pop()
				self.deck.discard.append(c)

		return winner, payout

	def deal(self):
		"""Deals two cards to player and banker"""
		for _ in range(2):
			for player in self.players:
				new_card = self.deck.draw()
				self.players[player].hand.append(new_card)

	def score(self):
		"""Says who is winning for this deck shuffle"""
		player_score = self.players['player'].score
		banker_score = self.players['banker'].score

		if self.verbose:
			print(f"Game score is:\nPlayer: {player_score}\nBanker: {banker_score}")


	def find_winner(self, player_total, banker_total):
		if self.verbose:
			print()
		winner = None
		if player_total > banker_total:
			if self.verbose:
				print(f"Player wins with {self.players['player'].get_hand()} "\
						f"totaling {player_total}")
			winner = ('player', 1, -1)
			self.tracker.player_wins += 1
			self.tracker.banker_only -= 1
			self.tracker.player_only += 1

			self.tracker.player_only_payout += 1
			self.tracker.banker_only_payout -= 1
		elif banker_total > player_total:
			if self.verbose:
				print(f"Banker wins with {self.players['banker'].get_hand()} "\
						f"totaling {banker_total}")
			if banker_total == 6:
				winner = ('banker', 0.5, 0.5)
				self.tracker.banker_wins += 1
				self.tracker.banker_half_payout += 1
				self.tracker.banker_only += 0.5
				self.tracker.player_only -= 1

				self.tracker.player_only_payout -= 1
				self.tracker.banker_only_payout += 0.5
				self.tracker.banker_only_half_payout += 1
			else:
				self.tracker.banker_wins += 1
				self.tracker.player_only -= 1
				self.tracker.banker_only += 1

				self.tracker.banker_only_payout += 1
				self.tracker.player_only_payout -= 1
				winner = ('banker', 1, 1)
		else:
			if self.verbose:
				print(f"Push. Player total = {player_total}. "\
					  f"Banker total = {banker_total}")
			self.tracker.ties += 1
			self.tracker.banker_only_payout += 0
			self.tracker.player_only_payout += 0
			winner = (None, 0, 0)

		if self.verbose:
			print()
		return winner

	def draw_one(self, who):
		me = self.players[who]
		new_card = self.deck.draw()
		me.hand.append(new_card)
		me.total = self.sum_hand(me.hand)
		return me.total, new_card

	def play(self):
		"""
			Meat of who draws what cards
			If either player is dealt a total of an 8 or a 9, both the player
			and banker stand.
			If the player's total is five or less, then the player will receive
			another card. Otherwise the player will stand.
			If the player stands, then the banker hits on a total of 5 or less
			The final betting option, a tie, palys out 8-to-1.
		"""
		self.tracker.total_games += 1
		player_score = self.players['player'].total
		banker_score = self.players['banker'].total

		if (self.verbose):
			print(f"Player has cards:\t{self.players['player'].get_hand()}")
			print(f"Player has score {player_score}")
			print(f"Banker has cards:\t{self.players['banker'].get_hand()}")
			print(f"Banker has score {banker_score}")

		# Natural
		if player_score in [8, 9] or banker_score in [8, 9]:
			return self.find_winner(player_score, banker_score)
		
		# Player has low score
		if player_score in [0, 1, 2, 3, 4, 5]:
			# Player gets a third card
			player_score, player_third = self.draw_one('player')
			if self.verbose:
				print(f"Player gets a third card:\t{player_third.abbreviation}")

			# Determine if banker needs a third card
			if (banker_score == 6 and player_third.rank in [6, 7]) or \
			   (banker_score == 5 and player_third.rank in [4, 5, 6, 7]) or \
			   (banker_score == 4 and player_third.rank in [2, 3, 4, 5, 6, 7]) or \
			   (banker_score == 3 and player_third.rank != 8) or \
			   (banker_score in [0, 1, 2]):
				banker_score, banker_third = self.draw_one('banker')
				if self.verbose:
					print(f"Banker gets a third card:\t{banker_third.abbreviation}")

		elif player_score in [6, 7]:
			if banker_score in [0, 1, 2, 3, 4, 5]:
				banker_score, banker_third = self.draw_one('banker')
				if self.verbose:
					print(f"Banker gets a third card:\t{banker_third.abbreviation}")

		if self.verbose:
			print(f"Player has final score of:\t{player_score}")
			print(f"Banker has final score of:\t{banker_score}")

		return self.find_winner(player_score, banker_score)


	def sum_hand(self, hand: list):
		cards = [card.rank if card.rank < 10 else 10 for card in hand]
		return sum(cards) % 10

if __name__ == "__main__":
	game = BaccaratGame(num_decks=8)
	while True:
		j = 0
		while j < 1_000_000:
			game.setup_game()
			print("Press enter/return key to continue")
			input()
			while game.deck.remaining() > 30:
				if game.verbose:
					os.system('clear')
				winner, payout = game.baccarat()
				game.score()
				print("Press enter/return key to continue")
				input()
				j += 1

			if game.verbose:
				print(f"Results of {game.tracker.shoe} shoe:")
				print(f"Player only bets payout : {game.tracker.player_only_payout}")
				print(f"Banker only bets payout : {game.tracker.banker_only_payout}")
				print(f"Banker only bets with half payout : {game.tracker.banker_only_half_payout}")
				print(f"Cards remaining in deck:\n{[card.abbreviation for card in game.deck.deck]}")
				print(f"Cards in discard:\n{[card.abbreviation for card in game.deck.discard]}")
				print(f"Cards burned {len(game.deck.burned_cards)}:\n{[card.abbreviation for card in game.deck.burned_cards]}")
			print("Press enter/return key to continue")
			input()

		print()
		print(f"Total games = {game.tracker.total_games}")
		print(f"Player win = {game.tracker.banker_wins} : {game.tracker.banker_win_percent()}%")
		print(f"Banker win = {game.tracker.player_wins} : {game.tracker.player_win_percent()}%")
		print(f"Total payout halved = {game.tracker.banker_half_payout} : {game.tracker.halved_win_percent()}%")
		print(f"Total tied games = {game.tracker.ties} : {game.tracker.tied_percent()}%")
		print(f"Player Only Total won : {game.tracker.player_only_percent()}%")
		print(f"Banker Only Total won : {game.tracker.banker_only_percent()}%")
		# print("Press enter/return key to continue")
		# input()