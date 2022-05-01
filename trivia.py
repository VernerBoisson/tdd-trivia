#!/usr/bin/env python3
from random import randint
from utils import Utils
from questions import Questions
from players import Players
import config_game as ConfigGame

class Game:
    def __init__(self):
        self.players = Players()
        self.current_player = 0
        self.list_all_questions = {}
        self._init_list_categories(ConfigGame.LIST_OF_CATEGORIES)

    def _init_list_categories(self, list_of_categories):
        for category in list_of_categories:
            self.list_all_questions[category] = Questions(category)
            self.list_all_questions[category].generate_questions(ConfigGame.NUMBER_OF_QUESTIONS_BY_CATEGORY)

    def _get_current_player(self):
        return self.players.get_player_by_index(self.current_player)

    def _get_current_player_name(self):
        return self._get_current_player().name

    def _get_question_category(self):
        return Utils.multi_key_dict_get(ConfigGame.dict_places_category, self._get_current_player().place)
    
    def start(self):
        while self._is_playable():
            self._log_player_turn()
            self._player_turn()
            if self._is_current_player_winner():        
                self._player_win()
                break
            if self._is_list_of_all_question_empty():
                Utils.print_log_game('no_more_questions')
                break
            self._change_current_player()
                    

    def _player_turn(self):
        roll_dice = self._roll_dice()
        self._log_roll_dice(roll_dice)
        self._player_try_to_leave_penalty_box(roll_dice)
        self._player_move(roll_dice)

    def _roll_dice(self):
        return randint(1, ConfigGame.DICE_FACE)

    def _log_roll_dice(self, roll_dice):
        Utils.print_log_game('roll_result', roll_result=roll_dice)

    def add_players(self, list_of_players):
        self.players.add_players(list_of_players)

    def _leave_penalty_box(self, roll_dice):
        current_player = self._get_current_player()
        if Utils.is_even(roll_dice):
            Utils.print_log_game('not_leave_penalty_box', player_name=current_player.name)
            return
        Utils.print_log_game('leave_penalty_box', player_name=current_player.name)
        current_player.is_in_penalty_box = False

    def _move_player_place(self, roll_dice):
        self._get_current_player().place += roll_dice
        if self._get_current_player().place >= ConfigGame.NUMBER_OF_PLACES:
            self._get_current_player().place -= ConfigGame.NUMBER_OF_PLACES
        self._log_move_player()
       
    def _log_move_player(self):
        Utils.print_log_game('new_location', player_name=self._get_current_player_name(),\
            new_location=self._get_current_player().place)

    def _log_player_turn(self):
        Utils.print_log_game('player_turn', player_name=self._get_current_player_name())

    def _player_try_to_leave_penalty_box(self, roll_dice):
        if self._get_current_player().is_in_penalty_box:
            self._leave_penalty_box(roll_dice)
    
    def _player_move(self, roll_dice):
        if not self._get_current_player().is_in_penalty_box:
            self._move_player_place(roll_dice)
            self._ask_question()

    def _player_win(self):
        if self._is_current_player_winner():
            Utils.print_log_game('winner', player_name=self._get_current_player_name(),\
                player_score=self._get_current_player().score)

    def _ask_question(self):
        category = self._get_question_category()
        if self.list_all_questions[category].is_empty():
            Utils.print_log_game('no_question_category', question_category=category)
            self._player_turn()
            return
        Utils.print_log_game('question_category', question_category=category)
        question = self.list_all_questions[category].get_last_question()
        Utils.print_log_game('question', question=question.question)
        self.list_all_questions[category].drop_last_question()
        self._simulate_player_answer()

    def _simulate_player_answer(self):
        if randint(0, 4) == 0:
            self._correct_answer()
            return
        self._wrong_answer()

    def _correct_answer(self):
        self._get_current_player().score += 1
        Utils.print_log_game('correct_answer')
        Utils.print_log_game('player_score', player_name=self._get_current_player_name(),\
            player_score=self._get_current_player().score)

    def _wrong_answer(self):
        self._get_current_player().is_in_penalty_box = True
        Utils.print_log_game('wrong_answer')
        Utils.print_log_game('sent_to_penalty_box', player_name=self._get_current_player_name())

    def _change_current_player(self):
        self.current_player += 1
        if self.current_player > self.players.last_index(): self.current_player = 0

    def _is_current_player_winner(self):
        return self._get_current_player().score >= ConfigGame.POINT_FOR_WINNING

    def _is_playable(self):
        return self.players.__len__() >= ConfigGame.MIN_NUMBER_OF_PLAYERS

    def _is_list_of_all_question_empty(self):
        for category in self.list_all_questions:
            if self.list_all_questions[category].__len__() > 0:
                return False
        return True

if __name__ == '__main__':
    game = Game()
    game.add_players(['Chet', 'Pat', 'Sue'])
    game.start()