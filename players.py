from utils import Utils

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

    def add_player(self, player_name):
        player = Player(player_name)
        self.players.append(player)
        self._log_add_player(player_name)
        
    def _log_add_player(self, player_name):
        Utils.print_log_game('add_player', player_name=player_name)
        Utils.print_log_game('number_of_players', number_of_player=self.__len__())

    def add_players(self, list_players_name):
        [self.add_player(player_name) for player_name in list_players_name]

    def __len__(self):
        return len(self.players)

    def last_index(self):
        return self.players.__len__() - 1