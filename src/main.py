"""
This is the interactive play module, which will allow users to simulate
blackjack play against the dealer with customizable configurations
"""

import os

from blackjack_utils import Decks, Hand, dealer_simulation, split_hands


def player_simulation(hands, dealer_upcard, deck, can_bet_more, rounds):
    """
    Function to allow user to simulate their turn in blackjack

    Returns whether the player chose to double down or not, in
    order to manipulate the game's bet amount
    """
    split = False
    double = False
    first_action = True  # To allow double down after the first 2 cards

    done = False

    while hands[0].value() < 21 and not done:
        os.system("clear")
        print(f"*****Round {rounds}*****")
        print("The dealer's up card is", dealer_upcard, "\n")
        print("Your", hands[0], "\n")

        while True:
            print("What action will you take?")
            print("(H)it  (S)tand", end="")

            if first_action and can_bet_more:
                print("  (D)ouble down", end="")

                if hands[0][0] == hands[0][1]:
                    same_card = True  # Check if player can split
                    print("  s(P)lit", end="")

            print("\n\n")

            action = input().upper()

            print("\n")

            if action == "H":
                deck.deal(hands[0])
                first_action = False
                break
            elif action == "S":
                done = True
                break
            elif action == "D" and first_action:
                double = True
                deck.deal(hands[0])
                done = True
                break
            elif action == "P" and same_card:
                split = True
                done = True
                break
            else:
                print("Invalid input, try again!", "\n")

    if split:
        split_hands(hands, deck)

        for i, hand in enumerate(hands):
            stand = False

            while hand.value() < 21 and not stand:
                os.system("clear")
                print(f"*****Round {rounds}*****")
                print(f"Now playing hand {i + 1}...")
                print("The dealer's up card is a", dealer_upcard, "\n")
                print("Your", hand, "\n")

                while True:
                    print("What action will you take?")
                    print("(H)it  (S)tand", end="")

                    print("\n\n")

                    action = input().upper()

                    print("\n")

                    if action == "H":
                        deck.deal(hand)
                        break
                    elif action == "S":
                        stand = True
                        break
                    else:
                        print("Invalid input, try again!", "\n")

        os.system("clear")
        print(f"*****Round {rounds}*****")
        print("Your first", hands[0], "\n")
        print("Your second", hands[1], "\n")

    else:
        os.system("clear")
        print(f"*****Round {rounds}*****")
        print("Your", hands[0], "\n")

    return double


def play_interactive_game():
    """
    Function to run the blackjack simulation in the terminal

    Asks the user to declare initial parameters such as money,
    bet amount, rounds, and decks, and clears output after every
    round
    """
    os.system("clear")
    print("Welcome to Blackjack!\n")
    initial_money = float(input("Enter initial money: "))
    bet_amount = float(input("Enter bet amount: "))
    max_rounds = int(input("Enter number of rounds: "))
    decks = int(input("Enter number of decks to use: "))

    rounds_played = 0
    current_money = initial_money
    penetration_limit = decks * 13  # 25% deck penetration for reshuffling

    shoe = Decks(decks)
    shoe.shuffle()

    while rounds_played < max_rounds and bet_amount <= current_money:
        rounds_played += 1
        os.system("clear")  # Clear the terminal for a clean round start

        if len(shoe) <= penetration_limit:
            shoe = Decks(decks)
            shoe.shuffle()

        player_hands = [Hand()]
        dealer_hand = Hand()

        for _ in range(2):
            shoe.deal(player_hands[0])
            shoe.deal(dealer_hand)

        dealer_upcard = dealer_hand[0]

        can_double = current_money >= bet_amount  # Ensure player can double their bet

        # Player's turn
        double = player_simulation(
            player_hands, dealer_upcard, shoe, can_double, rounds_played
        )

        # Dealer's turn
        dealer_simulation(dealer_hand, shoe)

        current_bet = bet_amount * (int(double) + 1)  # Double the bet if doubled down

        print("Dealer's turn complete!\n")
        print("The dealer's", dealer_hand, "\n")

        for i, hand in enumerate(player_hands):
            if len(player_hands) == 2:
                print(f"Hand {i + 1}:")

            if hand.value() > 21:
                print("Bust!", "\n")
                current_money -= current_bet
            elif dealer_hand.value() > 21 or dealer_hand.value() < hand.value():
                print("Win!", "\n")
                current_money += current_bet  # Payout for win
            elif dealer_hand.value() > hand.value():
                print("Lose!", "\n")
                current_money -= current_bet
            else:
                print("Tie!", "\n")

        if rounds_played != max_rounds:
            print(f"Money left: ${current_money:.2f}")
            print(f"Net gain/loss: ${(current_money - initial_money):.2f}", "\n")
            print("Press enter to continue to next round...")
            input()
        else:
            print("Press enter to cash out...")
            input()

    os.system("clear")

    final_amount = current_money - initial_money

    print(f"Final money left: ${current_money:.2f}")
    print(f"Final gain/loss: ${final_amount:.2f}\n")

    if rounds_played < max_rounds:
        print("Ouch, you lost your money before finishing all the rounds :(\n")

    if final_amount > 0:
        print("You're great at this, try your odds at a real casino!")
    elif final_amount < 0:
        print("Don't lose hope, you're one bet away from your next big win!")
    else:
        print("You barely scraped by, try harder next time!")

    print("\n\n")


if __name__ == "__main__":
    play_interactive_game()
