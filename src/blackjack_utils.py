"""
This is the main blackjack setup module containing OOP based
implementations of card, hand, and deck classes, as well as
functions to define the game logic and start a simulation run
"""

import random

# All cards and suits, aces are considered 11 to begin
card_values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "Queen": 10,
    "Jack": 10,
    "King": 10,
    "Ace": 11,
}

suits = {"Club", "Spade", "Diamond", "Heart"}


# Playing card class with each card having rank, suit, value (e.g. Jack, Diamond, 10)
class Card:
    def __init__(self, rank, suit, value):
        self.rank = rank
        self.suit = suit
        self.value = value

    def __eq__(self, other):
        return self.value == other.value  # To check value equivalence for split

    def __str__(self):
        return f"{self.rank} of {self.suit}s"


# Hand assumes that ace is 11 until it would cause player to bust, then it
# simulates changing the value of ace to 1
class Hand:
    def __init__(self):
        self.player_cards = []
        self.eleven_aces = 0  # Number of aces being used with 11 value, not 1
        self.card_total = 0

    def receive_card(self, new_card):
        if new_card.rank == "Ace":
            self.eleven_aces += 1

        self.player_cards.append(new_card)
        self.card_total += new_card.value

        if self.card_total > 21 and self.eleven_aces > 0:
            self.card_total -= 10  # There is an ace worth 11, so the ace is now 1
            self.eleven_aces -= 1  # Remove ace from list of aces

    def value(self):
        return self.card_total

    def has_eleven_ace(self):
        return self.eleven_aces > 0

    def split(self, other):
        other.receive_card(self.player_cards.pop())

        # Managing case where aces are split vs. other cards
        if self.player_cards[0].rank == "Ace":
            self.card_total -= 1
        else:
            self.card_total -= self.player_cards[0].value

    def __getitem__(self, card_number):
        return self.player_cards[card_number]

    def __len__(self):
        return len(self.player_cards)

    def __str__(self):
        return (
            "hand is worth "
            + str(self.value())
            + " and contains:\n"
            + "\n".join([str(card) for card in self.player_cards])
        )


# This will be used to simulate the shoe of cards, so we can make shoes
# by picking any arbitrary number of decks
class Decks:
    def __init__(self, num_decks=1):
        # List comprehension to create one deck of cards
        self.cards = [
            Card(rank, suit, value)
            for rank, value in card_values.items()
            for suit in suits
        ]

        self.cards *= num_decks

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, hand):
        hand.receive_card(self.cards.pop())  # Cards will be dealt directly to hands

    def __str__(self):
        return "\n".join([str(card) for card in self.cards])

    def __len__(self):
        return len(self.cards)


# Setting the dealer logic -
# The dealer has predetermined rules for hitting and standing. Simulating Soft 17 rules,
# so if dealer reaches 17 with an ace worth 11 then they have to hit again.
def dealer_simulation(hand, deck):
    while hand.value() < 17 or (hand.value() == 17 and hand.has_eleven_ace()):
        deck.deal(hand)


# Making easier hand splitting method
def split_hands(hands, deck):
    hands.append(Hand())  # Add a new hand for splitting
    hands[0].split(hands[1])  # Split the cards between hands

    for hand in hands:
        deck.deal(hand)


# Blackjack Configuration
# - Cards reshuffled after 25% deck penetration
# - 1:1 payout
# - Dealer hits soft 17
# - Player actions: (H)it, (S)tand, s(P)lit, (D)ouble down
# - No resplits
# - No double down after split
# - No surrender


# Customizable Configuration
# - Player strategy
# - Initial money (Default: 1000)
# - Bet amount (Default: 100)
# - Max rounds played (Default: 1)
# - Number of decks used for the shoe (Default: 6)
def simulation(strategy, initial_money=1000, bet_amount=100, max_rounds=1, decks=6):
    rounds_played = 0
    current_money = initial_money
    penetration_limit = decks * 13  # 25% deck penetration for reshuffling

    shoe = Decks(decks)
    shoe.shuffle()

    while rounds_played < max_rounds and bet_amount <= current_money:
        rounds_played += 1

        if len(shoe) <= penetration_limit:
            shoe = Decks(decks)
            shoe.shuffle()

        player_hands = [Hand()]  # Create list of hands due to possibility of split
        dealer_hand = Hand()

        for _ in range(2):
            shoe.deal(player_hands[0])
            shoe.deal(dealer_hand)

        dealer_upcard = dealer_hand[0]

        can_double = current_money >= bet_amount  # Ensure player can double their bet

        # Player's turn
        double = strategy(
            player_hands, shoe, dealer_upcard=dealer_upcard, can_bet_more=can_double
        )

        # Dealer's turn
        dealer_simulation(dealer_hand, shoe)

        current_bet = bet_amount * (int(double) + 1)  # Double the bet if doubled down

        for hand in player_hands:
            if hand.value() > 21:
                current_money -= current_bet
            elif dealer_hand.value() > 21 or dealer_hand.value() < hand.value():
                current_money += current_bet  # Payout for win
            elif dealer_hand.value() > hand.value():
                current_money -= current_bet
            # Else tie, so do nothing

    return current_money - initial_money
