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
    'add_question': '$question_category Question $question_number',
    'number_of_players':'They are player number $number_of_player',
    'player_turn':'$player_name is the current player',
    'new_location': '$player_name\'s new location is $new_location',
    'roll_result': 'They have rolled a $roll_result',
    'sent_to_penalty_box': '$player_name was sent to the penalty box',
    'leave_penalty_box': '$player_name is getting out of the penalty box',
    'not_leave_penalty_box': '$player_name is not getting out of the penalty box',
    'question_category': 'The category is $question_category',
    'wrong_answer': 'Question was incorrectly answered',
}

dict_places_category = {
    (0,4,8): CONSTANT['LIST_OF_CATEGORIES'][0],
    (1,5,9): CONSTANT['LIST_OF_CATEGORIES'][1],
    (2,6,10): CONSTANT['LIST_OF_CATEGORIES'][2],
    (3,7,11): CONSTANT['LIST_OF_CATEGORIES'][3],
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

    @staticmethod
    def multi_key_dict_get(dict, key):
        for keys, value in dict.items():
            if key in keys:
                return value
        return None

class Game:
    def __init__(self):
        self.players = Players()
        self.current_player = 0
        self.list_all_questions = {}
        self._init_list_categories(CONSTANT['LIST_OF_CATEGORIES'])
        self._generate_questions_by_category()

    def _init_list_categories(self, list_of_categories):
        for category in list_of_categories:
            self.list_all_questions[category] = Questions(category)

    def _generate_questions_by_category(self):
        for list_questions in self.list_all_questions.values():
            self._generate_questions(list_questions)

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

    def _get_current_player_name(self):
        return self.get_current_player().name

    def _leave_penalty_box(self, roll_dice):
        if Utils.is_even(roll_dice):
            Utils.print_log_game('not_leave_penalty_box', roll_result=roll_dice)
            return
        Utils.print_log_game('leave_penality_box', player_name=self._get_current_player_name())
        self.get_current_player().is_in_penalty_box = False

    def _move_player_place(self, roll_dice):
        self.get_current_player().place += roll_dice
        if self.get_current_player().place > 11:
            self.get_current_player().place -= 12      
        Utils.print_log_game('new_location', player_name=self._get_current_player_name(),\
            new_location=self.get_current_player().place)

    def player_turn(self, roll_dice):
        Utils.print_log_game('player_turn', player_name=self._get_current_player_name())
        Utils.print_log_game('roll_result', roll_result=roll_dice)

        if self.get_current_player().is_in_penalty_box:
            self._leave_penalty_box(roll_dice)
        
        if not self.get_current_player().is_in_penalty_box:
            self._move_player_place(roll_dice)
            self._ask_question()
        
        self._change_current_player()

    def _ask_question(self):
        Utils.print_log_game('question_category', question_category=self._current_category())
        print(self.list_all_questions[self._current_category()].questions[-1].question)
        self.list_all_questions[self._current_category()].questions.pop()

    def _current_category(self):
        return Utils.multi_key_dict_get(dict_places_category, self.get_current_player().place)

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
                if self.current_player == self.players._last_index(): self.current_player = 0
                return winner

            self.current_player += 1
            if self.current_player == self.players._last_index(): self.current_player = 0
            return True
        print("Answer was corrent!!!!")
        self.purses[self.current_player] += 1
        print(self.players[self.current_player] + \
            ' now has ' + \
            str(self.purses[self.current_player]) + \
            ' Gold Coins.')

        winner = self._did_player_win()

        return winner

    def wrong_answer(self):
        Utils.print_log_game('wrong_answer')
        Utils.print_log_game('sent_to_penalty_box', player_name=self._get_current_player_name())
        self.get_current_player().is_in_penalty_box = True

    def _change_current_player(self):
        self.current_player += 1
        if self.current_player > self.players._last_index(): self.current_player = 0

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
        self.is_in_penalty_box = False

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

    def _last_index(self):
        return self.players.__len__() - 1

if __name__ == '__main__':
    not_a_winner = False

    game = Game()

    game.add_player('Chet')
    game.add_player('Pat')
    game.add_player('Sue')
    counter = 0
    while True:
        game.player_turn(randrange(5) + 1)
        
        if randrange(9) == 7:
            # not_a_winner = game.wrong_answer()
            not_a_winner = False
        else:
            # not_a_winner = game.was_correctly_answered()
            not_a_winner = True
        if not not_a_winner: break
    