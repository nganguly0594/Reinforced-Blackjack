import gymnasium as gym
import numpy as np
from gymnasium import spaces

from blackjack_utils import Decks, Hand, dealer_simulation


# Environment for only hitting, standing, and doubling down
class BlackjackEnv(gym.Env):
    def __init__(self):
        # 3 possible actions total
        self.action_space = spaces.Discrete(3)
        # 25 hands, 10 dealer cards, explained in notebook 3
        self.observation_space = spaces.Tuple(
            (spaces.Discrete(25), spaces.Discrete(10))
        )

        self.shoe = Decks(6)
        self.shoe.shuffle()

    # To get the assigned hand number for each different hand
    # we are considering
    def _get_hand_num(self, hand):
        # If pair of aces
        if hand[0].value == 11 and hand[1].value == 11:
            return 8
        # If one card is ace, range is from 17-24
        elif hand[0].value == 11:
            return hand[1].value + 15
        elif hand[1].value == 11:
            return hand[0].value + 15
        # If just summing card total, range is from 0-16
        else:
            return hand.value() - 4

    # Subtract 2 to put in the range 0-9 instead of 2-Ace
    def _get_dealer_num(self, card):
        return card.value - 2

    # In order to prevent doubling down after first turn
    def _action_mask(self):
        if self.first_action:
            return np.ones(3, dtype=np.int8)

        # Masking the third option
        return np.array([1, 1, 0], dtype=np.int8)

    # Returns 2-tuple of observations
    def _get_obs(self):
        return (
            self._get_hand_num(self.player_hand),
            self._get_dealer_num(self.dealer_upcard),
        )

    # Called before every new episode, resets
    # all environment variables and player and dealer hands
    def reset(self):
        # Reset deck after set deck penetration limit of 25%
        if len(self.shoe) <= 78:
            self.shoe = Decks(6)
            self.shoe.shuffle()

        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.first_action = True  # To mask action in case of double down
        self.done = False  # Termination flag
        self.multiplier = 1  # Indicates how much bet is worth for doubling

        for _ in range(2):
            self.shoe.deal(self.player_hand)
            self.shoe.deal(self.dealer_hand)

        self.dealer_upcard = self.dealer_hand[0]  # First dealer card is visible

        # Returning observation, and action mask in the info dict
        return self._get_obs(), {"action_mask": self._action_mask()}

    def step(self, action):
        if action == 0:  # Hit
            self.shoe.deal(self.player_hand)
        elif action == 1:  # Stand
            self.done = True
        elif action == 2:  # Double Down
            self.shoe.deal(self.player_hand)
            self.multiplier = 2
            self.done = True

        self.first_action = False

        # If bust, round is over, don't need agent to evaluate
        if self.player_hand.value() >= 21:
            self.done = True

        reward = 0

        # Finishing dealer's turn and deciding rewards
        if self.done:
            dealer_simulation(self.dealer_hand, self.shoe)

            if self.player_hand.value() > 21:
                reward = -1 * self.multiplier
            elif (
                self.dealer_hand.value() > 21  # Dealer busts
                or self.dealer_hand.value() < self.player_hand.value()
            ):
                reward = 1 * self.multiplier  # Payout for win
            elif self.dealer_hand.value() > self.player_hand.value():
                reward = -1 * self.multiplier
            # Else tie, so no rewards provided

        return (
            self._get_obs(),
            reward,
            self.done,
            False,  # Truncation flag not required, no time limits
            {"action_mask": self._action_mask()},
        )
