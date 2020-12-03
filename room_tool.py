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
        if not self.isValid(token):
            print("Token invalido")
            return -1

        f = open("room/"+roomData["room"]+".json", "x")
        f.write(roomData)
        f.close()

        return 0

    def remove(self, token, roomName,current=None):
        print("Borrando mapa")
        if not self.isValid(token):
            print("Token invalido")
            return -1

        os.remove("room/"+roomName)

        return 0
    
    def isValid(self, token):
        proxyAuth = Ice.Application.communicator().stringToProxy(sys.argv[1])
        auth = Juego.AuthenticationPrx.uncheckedCast(proxyAuth)

        if not auth:
            raise RuntimeError('Invalid proxy')

        if auth.isValid(token):
            return True
        else:
            return False

class Server(Ice.Application):
    def run(self, argv):

        if len(sys.argv) != 2:
            print("Formato incorrecto. El formato es ./room_tool.py --Ice.Config=room_tool.config <proxyAuth_server>")
            return -1

        broker = self.communicator()
        servant = GestMapas()

        adapter = broker.createObjectAdapter("RoomServerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("RoomAdapter1"))

        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
server.main(sys.argv)
sys.exit()
