import unittest
from trivia import Game
from players import Player, Players
from questions import Question, Questions
from unittest.mock import patch, call

class TestGame(unittest.TestCase):
    def test_game_init(self):
        game = Game()
        self.assertIsInstance(game.players, Players)
        self.assertEqual(game.current_player_index, 0)
        self.assertIsInstance(game.list_all_questions, dict)
        self.assertEqual(game.list_all_questions, {})

    def test_init_list_all_questions(self):
        game = Game()
        game._init_list_all_questions(['Pop', 'Science'])
        self.assertIsInstance(game.list_all_questions, dict)
        self.assertIsInstance(game.list_all_questions['Pop'], Questions)
        self.assertIsInstance(game.list_all_questions['Science'], Questions)

    def test_get_current_player(self):
        game = Game()
        game.players.add_players([Player('player1'), Player('player2')])
        game.current_player_index = 1
        self.assertIsInstance(game._get_current_player(), Player)

    def test_get_current_player_name(self):
        game = Game()
        game.players.add_players([Player('player1'), Player('player2')])
        game.current_player_index = 1
        # TODO: implement

    def test_get_question_category(self):
        game = Game()
        game.players.add_players([Player('player1'), Player('player2')])
        self.assertEqual(game._get_question_category(), 'Pop')
        game.players.players[0].place = 1
        self.assertEqual(game._get_question_category(), 'Science')

    
    def test_start(self):
        pass            

    def test_player_turn(self):
        pass

    def test_roll_dice(self):
        game = Game()
        self.assertIn(game._roll_dice(), range(1, 7))

    def test_log_roll_dice(self):
        pass

    def test_add_players(self):
        game = Game()
        game.add_players([Player('player1'), Player('player2')])
        self.assertEqual(game.players.players, [Player('player1'), Player('player2')])

    def test_leave_penalty_box(self):
        game = Game()
        game.players.add_players([Player('player1'), Player('player2')])
        game.players[0].is_in_penalty_box = True
        game._leave_penalty_box(2)
        self.assertEqual(game.players[0].is_in_penalty_box, False)
        game.players[0].is_in_penalty_box = True
        game._leave_penalty_box(1)
        self.assertEqual(game.players[0].is_in_penalty_box, True)

    def test_move_player_place(self):
        game = Game()
        game.players.add_players([Player('player1'), Player('player2')])
        game.players[0].place = 3
        game._move_player_place(5)
        self.assertEqual(game.players[0].place, 8)
        game._move_player_place(5)
        self.assertEqual(game.players[0].place, 1)
       
    def test_log_move_player(self):
        pass

    def test_log_player_turn(self):
        pass
        
    def test_ask_question(self):
        pass

    def test_simulate_player_answer(self):
        pass

    def test_correct_answer(self):
        game = Game()
        game.players.add_players([Player('player1'), Player('player2')])
        game.players.players[0].score = 0
        self.assertEqual(game.players.players[0].score, 0)
        game._correct_answer()
        self.assertEqual(game.players.players[0].score, 1)

    def test_wrong_answer(self):
        game = Game()
        game.players.add_players([Player('player1'), Player('player2')])
        self.assertEqual(game.players.players[0].is_in_penalty_box, False)
        game._wrong_answer()
        self.assertEqual(game.players.players[0].is_in_penalty_box, True)

    def test_change_current_player(self):
        game = Game()
        game.players.add_players([Player('player1'), Player('player2')])
        game.current_player_index = 0
        game._change_current_player()
        self.assertEqual(game.current_player_index, 1)

    def test_is_current_player_winner(self):
        game = Game()
        game.players.add_players([Player('player1')])
        game.players.players[0].score = 1
        self.assertEqual(game._is_current_player_winner(), False)
        game.players.players[0].score = 9
        self.assertEqual(game._is_current_player_winner(), True)

    def test_is_playable(self):
        game = Game()
        game.players.add_players([Player('player1')])
        self.assertEqual(game._is_playable(), False)
        game.players.add_players([Player('player2'), Player('player3')])
        self.assertEqual(game._is_playable(), True)

    def test_is_list_of_all_question_empty(self):
        game = Game()
        game.list_all_questions = {
            'Pop': Questions('Pop'),
            'Science': Questions('Science')
        }
        self.assertEqual(game._is_list_of_all_question_empty(), True)
        game.list_all_questions['Pop'].add_question(Question('question1'))
        self.assertEqual(game._is_list_of_all_question_empty(), False)
        

if __name__ == '__main__':
    unittest.main()