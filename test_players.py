import unittest
from unittest.mock import patch, call
from players import Player, Players

class TestPlayer(unittest.TestCase):
    def test_player_init(self):
        player = Player('name')
        self.assertEqual(player.name, 'name')
        self.assertEqual(player.score, 0)
        self.assertEqual(player.place, 0)
        self.assertEqual(player.is_in_penalty_box, False)

class TestPlayers(unittest.TestCase):
    def test_players_init(self):
        players = Players()
        self.assertEqual(players.players, [])

    def test_players_add_player(self):
        players = Players()
        players.add_player('name')
        self.assertEqual(len(players.players), 1)
        self.assertIsInstance(players.players[0], Player)

    def test_players_add_players(self):
        players = Players()
        players.add_players(['name1', 'name2'])
        self.assertEqual(len(players.players), 2)
        self.assertIsInstance(players.players[0], Player)
        self.assertIsInstance(players.players[1], Player)

    def test_players_get_player_by_index(self):
        players = Players()
        players.add_players(['name1', 'name2'])
        self.assertIsInstance(players.get_player_by_index(0), Player)
        self.assertIsInstance(players.get_player_by_index(1), Player)
        self.assertEqual(players.get_player_by_index(0), players.players[0])
        self.assertEqual(players.get_player_by_index(1), players.players[1])

    @patch('builtins.print')
    def test_log_add_player(self, mock_print):
        players = Players()
        players._log_add_player('name')
        self.assertEqual(mock_print.mock_calls,\
            [call('name was added to the game.'),\
            call('They are player number 0')])

    def test_players_last_index(self):
        players = Players()
        players.add_players(['name1', 'name2'])
        self.assertEqual(players.last_index(), 1)

if __name__ == '__main__':
    unittest.main()