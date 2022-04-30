#!/usr/bin/env python3
from random import randint
from utils import Utils

CONSTANT = {
    'NUMBER_OF_QUESTIONS_BY_CATEGORY': 50,
    'LIST_OF_CATEGORIES': ['Pop', 'Science', 'Sports', 'Rock'],
    'MIN_NUMBER_OF_PLAYERS': 2,
    'POINT_FOR_WINNING': 6,
    'DICE_FACE': 6,
    'NUMBER_OF_PLACES': 12,
}


dict_places_category = {
    (0,4,8): CONSTANT['LIST_OF_CATEGORIES'][0],
    (1,5,9): CONSTANT['LIST_OF_CATEGORIES'][1],
    (2,6,10): CONSTANT['LIST_OF_CATEGORIES'][2],
    (3,7,11): CONSTANT['LIST_OF_CATEGORIES'][3],
}

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
        [self._generate_questions(category) for category in self.list_all_questions.values()]

    def _generate_questions(self, category):
        [category.add_question(Question(\
            Utils.template_log('add_question',\
            question_category=category.category_name,\
            question_number=category.questions.__len__())))\
            for _ in range(CONSTANT['NUMBER_OF_QUESTIONS_BY_CATEGORY'])]

    def _is_playable(self):
        return self.players.__len__() >= CONSTANT['MIN_NUMBER_OF_PLAYERS']

    def start(self):
        while self._is_playable():
            self._player_turn(self._roll_dice())
            if self._is_current_player_winner():        
                self._player_win()
                break
            self._change_current_player()
                

    def _roll_dice(self):
        return randint(1, CONSTANT['DICE_FACE'])

    def add_player(self, player_name):
        player = Player(player_name)
        self.players.add_player(player)

    def add_players(self, list_players_name):
        [self.add_player(player_name) for player_name in list_players_name]

    def _get_current_player(self):
        return self.players.get_player_by_index(self.current_player)

    def _get_current_player_name(self):
        return self._get_current_player().name

    def _leave_penalty_box(self, roll_dice):
        if Utils.is_even(roll_dice):
            Utils.print_log_game('not_leave_penalty_box', player_name=self._get_current_player_name())
            return
        Utils.print_log_game('leave_penalty_box', player_name=self._get_current_player_name())
        self._get_current_player().is_in_penalty_box = False

    def _move_player_place(self, roll_dice):
        self._get_current_player().place += roll_dice
        if self._get_current_player().place >= CONSTANT['NUMBER_OF_PLACES']:
            self._get_current_player().place -= CONSTANT['NUMBER_OF_PLACES']
        self._log_move_player()
       
    def _log_move_player(self):
        Utils.print_log_game('new_location', player_name=self._get_current_player_name(),\
            new_location=self._get_current_player().place)

    def _player_turn(self, roll_dice):
        Utils.print_log_game('player_turn', player_name=self._get_current_player_name())
        Utils.print_log_game('roll_result', roll_result=roll_dice)

        if self._get_current_player().is_in_penalty_box:
            self._leave_penalty_box(roll_dice)
        
        if not self._get_current_player().is_in_penalty_box:
            self._move_player_place(roll_dice)
            self._ask_question()
            self._simulate_player_answer()


    def _player_win(self):
        if self._is_current_player_winner():
            Utils.print_log_game('winner', player_name=self._get_current_player_name(),\
                player_score=self._get_current_player().score)

    def _ask_question(self):
        Utils.print_log_game('question_category', question_category=self._current_category())
        print(self.list_all_questions[self._current_category()].questions[-1].question)
        self.list_all_questions[self._current_category()].questions.pop()

    def _simulate_player_answer(self):
        if randint(0, 4) == 0:
            self._correct_answer()
            return
        self._wrong_answer()

    def _current_category(self):
        return Utils.multi_key_dict_get(dict_places_category, self._get_current_player().place)

    def _correct_answer(self):
        self._get_current_player().score += 1
        Utils.print_log_game('correct_answer')
        Utils.print_log_game('player_score', player_name=self._get_current_player_name(), player_score=self._get_current_player().score)
 

    def _wrong_answer(self):
        self._get_current_player().is_in_penalty_box = True
        Utils.print_log_game('wrong_answer')
        Utils.print_log_game('sent_to_penalty_box', player_name=self._get_current_player_name())

    def _change_current_player(self):
        self.current_player += 1
        if self.current_player > self.players._last_index(): self.current_player = 0

    def _is_current_player_winner(self):
        return self._get_current_player().score >= CONSTANT['POINT_FOR_WINNING']

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
        self.score = 0
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
    game = Game()
    game.add_players(['Chet', 'Pat', 'Sue'])
    game.start()