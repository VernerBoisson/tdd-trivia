#!/usr/bin/env python3
from random import randrange
from string import Template

CONSTANT = {
    'NUMBER_OF_QUESTIONS': 50,
    'LIST_OF_CATEGORIES': ['Pop', 'Science', 'Sports', 'Rock'],
    'MIN_NUMBER_OF_PLAYERS': 2,
}

log_game = {
    'add_player':'$player_name was added to the game.',
    'number_of_players':'They are player number $number_of_player',
    'player_turn':'$player_name is the current player',
    'roll_result': 'They have rolled a $roll_result',
    'add_question': '$question_category Question $question_number',
    'leave_penalty_box': '$player_name is getting out of the penalty box',
    'not_leave_penalty_box': '$player_name is not getting out of the penalty box',
    'new_location': '$player_name\'s new location is $new_location',
}

class Utils:
    @staticmethod
    def is_even(number):
        return number % 2 == 0

    @staticmethod
    def template_log(log_type, **kwargs):
        return Template(log_game[log_type]).substitute(kwargs)


    @staticmethod
    def print_log_game(log_key, **kwargs):
        print(Utils.template_log(log_key, **kwargs))

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
            category.add_question(Question(\
                Utils.template_log('add_question',\
                     question_category=category.category_name,\
                     question_number=category.questions.__len__())))

    def _is_playable(self):
        return self.players.__len__() >= CONSTANT['MIN_NUMBER_OF_PLAYERS']

    def add_player(self, player_name):
        player = Player(player_name)
        self.players.add_player(player)

    def get_current_player(self):
        return self.players.get_player_by_index(self.current_player)

    def _leave_penalty_box(self, roll):
        if Utils.is_even(roll):
            Utils.print_log_game('not_leave_penalty_box', roll_result=roll)
            return
        Utils.print_log_game('leave_penality_box', player_name=self.get_current_player().name)

    def _move_player_place(self, roll):
        self.get_current_player().place += roll
        if self.get_current_player().place > 11:
            self.get_current_player().place -= 12      
        Utils.print_log_game('new_location', player_name=self.get_current_player().name,\
            new_location=self.get_current_player().place)

    def roll(self, roll):
        Utils.print_log_game('player_turn', player_name=self.get_current_player().name)
        Utils.print_log_game('roll_result', roll_result=roll)

        if self.get_current_player().in_penalty_box:
            self._leave_penalty_box(roll)
        
        if not self.get_current_player().in_penalty_box:
            self._move_player_place(roll)
            self._ask_question()

    def _ask_question(self):
        print("The category is %s" % self._current_category)
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

    def get_player_by_index(self, index):
        return self.players[index]

    def add_player(self, player):
        self.players.append(player)
        Utils.print_log_game('add_player', player_name=player.name)
        Utils.print_log_game('number_of_players', number_of_player=self.__len__())

    def __len__(self):
        return len(self.players)

if __name__ == '__main__':
    not_a_winner = False

    game = Game()

    game.add_player('Chet')
    game.add_player('Pat')
    game.add_player('Sue')

    while True:
        game.roll(randrange(5) + 1)

        # if randrange(9) == 7:
        #     not_a_winner = game.wrong_answer()
        # else:
        #     not_a_winner = game.was_correctly_answered()

        # if not not_a_winner: break
        break