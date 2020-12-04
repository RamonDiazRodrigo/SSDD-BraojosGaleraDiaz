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




def parse_commandline(server_pid):
    '''Parse and check commandline'''
    parser = argparse.ArgumentParser('IceDungeon Local Game')

    #aqui se coge el mapa con getRoom() y se añade a la lista de argumentos

    parser.add_argument(
    'LEVEL', 
    nargs='+', 
    default=[DEFAULT_ROOM], 
    choices = server_pid.getRoom(), 
    help='List of levels')


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



def map_server_pid(): #metodo para conseguir el pid del servidor de mapas
    '''
    Buscar un proxy de mapas activos y obtener un PID
    '''
    for proc in psutil.process_iter():
        if proc.name().startswith('python3'):
            for arg in proc.cmdline():
                if arg.startswith('./'):
                    arg = arg[2:]
                if arg == 'map_server': #ver si esto se llama map server o no
                    return proc.pid
    return None







def run():
    '''Start game according to commandline'''

    #fork al servidor de mapas

    server_pid = map_server_pid()
    if not server_pid:
        print('ERROR: no se ha encontrado ningun servidor de mapas.')
        return EXIT_ERROR
    
    #una vez hecho el fork al servidor de mapas se tiene que coger un mapa
    #el mapa se coge de la interfaz SerJuego del slice, del metodo getRoom()
    #una vez se coja el mapa se tiene que pasar como argumento en el parse_commandline
    
    

    user_options = parse_commandline(server_pid)
    if not user_options:
        return BAD_COMMAND_LINE

    game.pyxeltools.initialize()
    dungeon = game.DungeonMap(user_options.LEVEL)
    gauntlet = game.Game(user_options.hero, dungeon)
    gauntlet.add_state(game.screens.TileScreen, game.common.INITIAL_SCREEN)
    gauntlet.add_state(game.screens.StatsScreen, game.common.STATUS_SCREEN)
    gauntlet.add_state(game.screens.GameScreen, game.common.GAME_SCREEN)
    gauntlet.add_state(game.screens.GameOverScreen, game.common.GAME_OVER_SCREEN)
    gauntlet.add_state(game.screens.GoodEndScreen, game.common.GOOD_END_SCREEN)
    gauntlet.start()

    return EXIT_OK

run()

