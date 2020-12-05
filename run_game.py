#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W1203

'''
    ICE Gauntlet LOCAL GAME

    Se debe crear un fork del juego local. El nuevo cliente deberá solicitar el proxy del servicio del
    juego y mantener el resto de opciones que tiene el cliente original.

'''
import sys
import os
import atexit
import logging
import argparse
import psutil

import Ice
Ice.loadSlice('juego.ice')
import Juego
import game
import game.common
import game.screens
import game.pyxeltools
import game.orchestration


EXIT_OK = 0
BAD_COMMAND_LINE = 1

DEFAULT_ROOM = 'tutorial.json'
DEFAULT_HERO = game.common.HEROES[0]


@atexit.register
# pylint: disable=W0613
def bye(*args, **kwargs):
    '''Exit callback, use for shoutdown'''
    print('Thanks for playing!')
# pylint: enable=W0613


def parse_commandline():
    '''Parse and check commandline'''
    parser = argparse.ArgumentParser('IceDungeon Local Game')
    parser.add_argument('LEVEL', nargs='+',
                        default=[DEFAULT_ROOM], help='List of levels')
    parser.add_argument(
        '-p', '--player', default=DEFAULT_HERO, choices=game.common.HEROES,
        dest='hero', help='Hero to play with'
    )
    options = parser.parse_args()

    for level_file in options.LEVEL:
        if not game.assets.search(level_file):
            logging.error(f'Level "{level_file}" not found!')
            return None
    return options


class Client(Ice.Application):
    def run(self, argv):
        '''Start game according to commandline'''

        # fork al servidor de mapas

        proxy = self.communicator().stringToProxy(argv[1])
        mapas = Juego.SerJuegoPrx.uncheckedCast(proxy)

        if not mapas:
            raise RuntimeError('Invalid proxy')
        level = []
        level.append(mapas.getRoom())
        # una vez hecho el fork al servidor de mapas se tiene que coger un mapa
        # el mapa se coge de la interfaz SerJuego del slice, del metodo getRoom()
        # una vez se coja el mapa se tiene que pasar como argumento en el parse_commandline

        game.pyxeltools.initialize()
        dungeon = game.DungeonMap(level)
        gauntlet = game.Game(DEFAULT_HERO, dungeon)
        gauntlet.add_state(game.screens.TileScreen, game.common.INITIAL_SCREEN)
        gauntlet.add_state(game.screens.StatsScreen, game.common.STATUS_SCREEN)
        gauntlet.add_state(game.screens.GameScreen, game.common.GAME_SCREEN)
        gauntlet.add_state(game.screens.GameOverScreen,
                           game.common.GAME_OVER_SCREEN)
        gauntlet.add_state(game.screens.GoodEndScreen,
                           game.common.GOOD_END_SCREEN)
        gauntlet.start()

        return EXIT_OK


sys.exit(Client().main(sys.argv))
