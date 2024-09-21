#!/usr/bin/env python3
import logging
import sys
from configparser import ConfigParser

from hexhex.logic import hexboard
from hexhex.logic.hexgame import MultiHexGame
from hexhex.utils.utils import load_model


class PlayGame:
    def __init__(self, config):
        self.config = config['group_007_config']
        self.board = None
        self.switch = self.config.getboolean('switch', False)
        self.model = load_model(f'agents/Group007/models/{self.config.get("model")}.pt')

    def respond(self, line):
        splitted = line.split(' ')
        if splitted[0] == 'boardsize':
            self.board = hexboard.Board(int(splitted[1]), self.switch)
            self.game = MultiHexGame(
                    boards=(self.board,),
                    models=(self.model,),
                    noise=None,
                    noise_parameters=None,
                    temperature=self.config.getfloat('temperature', 0.),
                    temperature_decay=self.config.getfloat('temperature_decay', 1.),
            )
            return ''
        if splitted[0] == 'play':
            color = splitted[1]
            position = splitted[2]
            if splitted[2] != 'resign':
                y = ord(position[0]) - ord('a')
                x = int(position[1:]) - 1
                self.board.set_stone((x, y))
        if splitted[0] == 'genmove':
            if self.board.winner:
                return 'resign'
            self.game.batched_single_move(self.model)
            move = self.board.move_history[-1][1]
            alpha, numeric = hexboard.position_to_alpha_numeric(move)
            return f'{alpha}{numeric}'

def start_game():
    config = ConfigParser()
    config.read('agents/Group007/config.ini')
    game = PlayGame(config)
    return game
