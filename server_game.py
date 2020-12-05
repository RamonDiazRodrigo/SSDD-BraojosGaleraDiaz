#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-
# pylint: disable=W0613
# pylint: disable=C0411
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0103

"""
   ICE Gauntlet Game Server
"""

import sys
import Ice
import os
import json
import glob
import random
Ice.loadSlice('juego.ice')
# pylint: disable=E0401
# pylint: disable=C0413
import Juego

class SerJuego(Juego.SerJuego):
    def getRoom(self, current=None):

        try:
            rooms = []
            for name in glob.glob('assets/*.json'):
                rooms.append(name)
            if "assets/palette.json" in rooms:
                rooms.remove("assets/palette.json")
            rng = random.randint(0, len(rooms)-1)
            return rooms[rng]
        except Exception as noexiste:
            print("Error: {}".format("Mapa no encontrado."))
            raise Juego.RoomNotExists() from noexiste

class Server(Ice.Application):
    def run(self, argv):

        if len(sys.argv) != 1:
            print("Formato: ./room_tool.py --Ice.Config=room_tool.config <proxyAuth_server>")
            return -1

        broker = self.communicator()
        servant = SerJuego()

        adapter = broker.createObjectAdapter("GameServerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("GameServer1"))

        print('"{}"'.format(proxy), flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
server.main(sys.argv)
sys.exit()
