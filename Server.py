#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
import os
Ice.loadSlice('juego.ice')
import Juego

class GestMapas(Juego.GestMapas):
    def publish(self, token, roomData, current=None):
        print("Publicando mapa")
        return 0

    def remove(self, current=None):
        print("Borrando mapa")
        return 0

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = GestMapas()

        adapter = broker.createObjectAdapter("")
        proxy = adapter.add(servant, broker.stringToIdentity(""))

        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
server.main(sys.argv)
sys.exit()
