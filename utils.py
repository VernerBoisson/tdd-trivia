from string import Template
import json

log_game = json.load(open('game_sentences.json'))

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