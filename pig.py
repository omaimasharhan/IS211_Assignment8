import random
import time
import argparse
import sys

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_total = 0

    def roll_die(self, die):
        roll = die.roll()
        if roll == 1:
            self.turn_total = 0
            return 1
        else:
            self.turn_total += roll
            return roll

    def hold(self):
        self.score += self.turn_total
        self.turn_total = 0

    def is_winner(self):
        return self.score >= 100

class ComputerPlayer(Player):
    def make_decision(self):
        if self.score < 100 and self.turn_total < 10:
            return "r"
        else:
            return "h"

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return Player(name)
        elif player_type == "computer":
            return ComputerPlayer(name)

class Die:
    def __init__(self, sides=6):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player = player1
        self.die = Die()

    def switch_player(self):
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]

    def play_turn(self):
        print(f"{self.current_player.name}'s turn:")
        while True:
            if isinstance(self.current_player, ComputerPlayer):
                decision = self.current_player.make_decision()
            else:
                decision = input("Enter 'r' to roll or 'h' to hold: ")

            if decision == 'r':
                roll_result = self.current_player.roll_die(self.die)
                print(f"Rolled: {roll_result}")
                print(f"Current Turn Total: {self.current_player.turn_total}")
                if roll_result == 1:
                    print(f"{self.current_player.name} rolled a 1. Turn over.")
                    break
            elif decision == 'h':
                self.current_player.hold()
                print(f"{self.current_player.name} decided to hold.")
                break

    def play_game(self):
        while not self.current_player.is_winner():
            print(f"Current Scores: {self.players[0].name}: {self.players[0].score}, {self.players[1].name}: {self.players[1].score}")
            self.play_turn()
            self.switch_player()

        print(f"{self.current_player.name} wins with a score of {self.current_player.score}!")

class TimedGameProxy:
    def __init__(self, player1, player2, time_limit=60):
        self.game = Game(player1, player2)
        self.start_time = time.time()
        self.time_limit = time_limit

    def switch_player(self):
        self.game.switch_player()

    def play_turn(self):
        if time.time() - self.start_time >= self.time_limit:
            self.determine_winner(time_limit_exceeded=True)
        else:
            self.game.play_turn()
            if self.game.current_player.is_winner():
                self.determine_winner()

    def play_game(self):
        while not self.game.current_player.is_winner() and (time.time() - self.start_time) < self.time_limit:
            remaining_time = self.time_limit - (time.time() - self.start_time)
            if remaining_time < 0:
                remaining_time = 0  # Ensure remaining time is non-negative
            print(f"Time Remaining: {int(remaining_time)} seconds")
            print(f"Current Scores: {self.game.players[0].name}: {self.game.players[0].score}, {self.game.players[1].name}: {self.game.players[1].score}")
            self.play_turn()
            self.switch_player()

        if not self.game.current_player.is_winner() and (time.time() - self.start_time) >= self.time_limit:
            self.determine_winner(time_limit_exceeded=True)
        else:
            self.determine_winner()

    def determine_winner(self, time_limit_exceeded=False):
        if self.game.players[0].is_winner() or time_limit_exceeded:
            print(f"{self.game.players[0].name} wins with a score of {self.game.players[0].score}!")
        elif self.game.players[1].is_winner() or time_limit_exceeded:
            print(f"{self.game.players[1].name} wins with a score of {self.game.players[1].score}!")
        else:
            print("It's a tie!")

if __name__ == "__main__":
    player1_type = input("Enter player 1 type (human or computer): ")
    player2_type = input("Enter player 2 type (human or computer): ")
    player1 = PlayerFactory.create_player(player1_type, "Player 1")
    player2 = PlayerFactory.create_player(player2_type, "Player 2")

    parser = argparse.ArgumentParser()
    parser.add_argument('--timed', action='store_true', help='Enable timed game mode')
    args = parser.parse_args()

    if args.timed:
        time_limit = 60
    if "--timed" in sys.argv:
        time_limit = int(input("Enter time limit in seconds: "))
        game = TimedGameProxy(player1, player2, time_limit)
    else:
        game = Game(player1, player2)

    game.play_game()