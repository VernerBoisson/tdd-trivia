#!/usr/bin/env python3
from random import randrange
from string import Template

CONSTANT = {
    'NUMBER_OF_QUESTIONS': 50,
    'LIST_OF_CATEGORIES': ['Pop', 'Science', 'Sports', 'Rock'],
    'MIN_NUMBER_OF_PLAYERS': 2,
}

log_game = {
    "add_player":"$player_name was added to the game.",
    "number_of_players":'They are player number $number_of_player',
}

class Units:
    @staticmethod
    def is_odd(number):
        return number % 2 != 0

    @staticmethod
    def print_log_game(log_key, **kwargs):
        print(Template(log_game[log_key]).substitute(kwargs))

class Game:
    def __init__(self):
        self.players = Players()
        self.current_player = 0
        self.list_all_questions = []
        self._init_list_categories(CONSTANT['LIST_OF_CATEGORIES'])
        self._generate_questions_by_category()

    def _init_list_categories(self, list_of_categories):
        for category in list_of_categories:
            self.list_all_questions.append(Questions(category))

    def _generate_questions_by_category(self):
        for category in self.list_all_questions:
            self._generate_questions(category)

    def _generate_questions(self, category):
        for _ in range(CONSTANT['NUMBER_OF_QUESTIONS']):
            category.add_question(Question(f'{category.category_name} Question {category.__len__()}'))

    def _is_playable(self):
        return self.players.__len__() >= CONSTANT['MIN_NUMBER_OF_PLAYERS']

    def _is_odd(self, n):
        return n % 2 != 0

    def add_player(self, player_name):
        player = Player(player_name)
        self.players.add_player(player)


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

                print(self.players[self.current_player] + \
                            '\'s new location is ' + \
                            str(self.places[self.current_player]))
                print("The category is %s" % self._current_category)
                self._ask_question()
            else:
                print("%s is not getting out of the penalty box" % self.players[self.current_player])
                self.is_getting_out_of_penalty_box = False
        else:
            self.places[self.current_player] = self.places[self.current_player] + roll
            if self.places[self.current_player] > 11:
                self.places[self.current_player] = self.places[self.current_player] - 12

            print(self.players[self.current_player] + \
                        '\'s new location is ' + \
                        str(self.places[self.current_player]))
            print("The category is %s" % self._current_category)
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
                if self.current_player == self.players.__len__(): self.current_player = 0
                return winner

            self.current_player += 1
            if self.current_player == self.players.__len__(): self.current_player = 0
            return True
        print("Answer was corrent!!!!")
        self.purses[self.current_player] += 1
        print(self.players[self.current_player] + \
            ' now has ' + \
            str(self.purses[self.current_player]) + \
            ' Gold Coins.')

        winner = self._did_player_win()
        self.current_player += 1
        if self.current_player == self.players.__len__(): self.current_player = 0

        return winner

    def wrong_answer(self):
        print('Question was incorrectly answered')
        print(self.players[self.current_player] + " was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True

        self.current_player += 1
        if self.current_player == self.players.__len__(): self.current_player = 0

    def _did_player_win(self):
        return not (self.purses[self.current_player] == 6)

class Question:
    def __init__(self, question):
        self.question = question
    
class Questions:
    def __init__(self, category_name):
        self.category_name = category_name
        self.questions = []
    
    def add_question(self, question):
        self.questions.append(question)

    def __len__(self):
        return len(self.questions)

class Player:
    def __init__(self, name):
        self.name = name
        self.purse = 0
        self.place = 0
        self.in_penalty_box = False

class Players:
    def __init__(self):
        self.players = []

    def add_player(self, player):
        self.players.append(player)
        Units.print_log_game('add_player', player_name=player.name)
        Units.print_log_game('number_of_players', number_of_player=self.__len__())

    def __len__(self):
        return len(self.players)

if __name__ == '__main__':
    not_a_winner = False

    game = Game()

    game.add_player('Chet')
    game.add_player('Pat')
    game.add_player('Sue')

    # while True:
    #     game.roll(randrange(5) + 1)

    #     if randrange(9) == 7:
    #         not_a_winner = game.wrong_answer()
    #     else:
    #         not_a_winner = game.was_correctly_answered()

    #     if not not_a_winner: break