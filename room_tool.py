#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
import os
import json
Ice.loadSlice('juego.ice')
import Juego



class GestMapas(Juego.GestMapas):
    def publish(self, token, roomData, current=None):
        
        
        print("Publicando mapa...")
        if not self.isValid(token):
            print("Error: {}".format("No estas autorizado."))
            raise Juego.Unauthorized()
        
        try:
            roomDataJson = json.loads(roomData)
            archivo = "assets/"+roomDataJson["room"]+".json"
        except Exception:
            print("Error: {}".format("Error en el formato del archivo JSON."))
            raise Juego.WrongRoomFormat()

        try:
            f = open(archivo, "x")
        except Exception:
            print("Error: {}".format("El mapa ya existe."))
            raise Juego.RoomAlreadyExists()
        
        
        f.write(roomData)
        f.close()
        print("Mapa publicado.")
        return 0

    def remove(self, token, roomName,current=None):
        print("Borrando mapa")
        if not self.isValid(token):
            print("Token invalido")
            return -1

        os.remove("assets/"+roomName)

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
