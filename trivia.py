#!/usr/bin/env python3
from random import randrange

class Game:
    def __init__(self):
        self.players = []
        self.places = [0] * 6
        self.purses = [0] * 6
        self.in_penalty_box = [0] * 6

        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []

        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

        for i in range(50):
            self.pop_questions.append("Pop Question %s" % i)
            self.science_questions.append("Science Question %s" % i)
            self.sports_questions.append("Sports Question %s" % i)
            self.rock_questions.append("Rock Question %s" % i)


    def is_playable(self):
        return self.how_many_players >= 2

    def add_player(self, player_name):
        self.players.append(player_name)
        self.places[self.how_many_players] = 0
        self.purses[self.how_many_players] = 0
        self.in_penalty_box[self.how_many_players] = False

        print(player_name + " was added")
        print("They are player number %s" % len(self.players))

    @property
    def how_many_players(self):
        return len(self.players)

    def _is_odd(self, n):
        return n % 2 != 0

    def roll(self, roll):
        print("%s is the current player" % self.players[self.current_player])
        print("They have rolled a %s" % roll)

        if self.in_penalty_box[self.current_player]:
            if self._is_odd(roll):
                self.is_getting_out_of_penalty_box = True

                print("%s is getting out of the penalty box" % self.players[self.current_player])
                self.places[self.current_player] = self.places[self.current_player] + roll
                if self.places[self.current_player] > 11:
                    self.places[self.current_player] = self.places[self.current_player] - 12
            self._log_question()
            self._ask_question()
            
            print("%s is not getting out of the penalty box" % self.players[self.current_player])
            self.is_getting_out_of_penalty_box = False
        self.places[self.current_player] = self.places[self.current_player] + roll
        if self.places[self.current_player] > 11:
            self.places[self.current_player] = self.places[self.current_player] - 12
        self._log_question()
        self._ask_question()

    def _log_question(self):
        print(self.players[self.current_player] + \
                    '\'s new location is ' + \
                    str(self.places[self.current_player]))
        print("The category is %s" % self._current_category)


    def _ask_question(self):
        if self._current_category == 'Pop': print(self.pop_questions.pop(0))
        if self._current_category == 'Science': print(self.science_questions.pop(0))
        if self._current_category == 'Sports': print(self.sports_questions.pop(0))
        if self._current_category == 'Rock': print(self.rock_questions.pop(0))

    @property
    def _current_category(self):
        if self.places[self.current_player] in [0,4,8]: return 'Pop'
        if self.places[self.current_player] in [1,5,9]: return 'Science'
        if self.places[self.current_player] in [2,6,10]: return 'Sports'
        return 'Rock'

    def was_correctly_answered(self):
        if self.in_penalty_box[self.current_player]:
            if self.is_getting_out_of_penalty_box:
                print('Answer was correct!!!!')
                self.purses[self.current_player] += 1
                print(self.players[self.current_player] + \
                    ' now has ' + \
                    str(self.purses[self.current_player]) + \
                    ' Gold Coins.')

                winner = self._did_player_win()
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0
                return winner

            self.current_player += 1
            if self.current_player == len(self.players): self.current_player = 0
            return True
        print("Answer was corrent!!!!")
        self.purses[self.current_player] += 1
        print(self.players[self.current_player] + \
            ' now has ' + \
            str(self.purses[self.current_player]) + \
            ' Gold Coins.')

        winner = self._did_player_win()
        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0

        return winner

    def wrong_answer(self):
        print('Question was incorrectly answered')
        print(self.players[self.current_player] + " was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True

        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0

    def _did_player_win(self):
        return not (self.purses[self.current_player] == 6)



if __name__ == '__main__':
    not_a_winner = False

    game = Game()

    game.add_player('Chet')
    game.add_player('Pat')
    game.add_player('Sue')

    while True:
        game.roll(randrange(5) + 1)

        if randrange(9) == 7:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()

        if not not_a_winner: break