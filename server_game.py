#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-


import sys
import Ice
import os
import json
import glob
import random
Ice.loadSlice('juego.ice')
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
        except Exception:
            print("Error: {}".format("Mapa no encontrado."))
            raise Juego.RoomNotExists()

class Server(Ice.Application):
    def run(self, argv):

        if len(sys.argv) != 1:
            print("Formato incorrecto. El formato es ./room_tool.py --Ice.Config=room_tool.config <proxyAuth_server>")
            return -1

        broker = self.communicator()
        servant = SerJuego()

        adapter = broker.createObjectAdapter("GameServerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("GameServer1"))

        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
server.main(sys.argv)
sys.exit()
