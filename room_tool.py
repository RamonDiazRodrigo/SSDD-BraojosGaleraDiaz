#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-
# pylint: disable=W0613
# pylint: disable=C0411
# pylint: disable=C0115
# pylint: disable=C0116

"""
   ICE Gauntlet Gestion Mapas Server
"""

import sys
import Ice
import os
import json
import hashlib
Ice.loadSlice("juego.ice")
# pylint: disable=E0401
# pylint: disable=C0413
import Juego


class GestMapas(Juego.GestMapas):
    def publish(self, token, roomdata, current=None):

        print("Publicando mapa...")
        if not self.isvalid(token):
            print("Error: {}".format("No estas autorizado."))
            raise Juego.Unauthorized()

        try:
            roomdatajson = json.loads(roomdata)
            room = roomdatajson["room"]
            _data = roomdatajson["data"]
        except Exception as formatoincorrecto:
            print("Error: {}".format("Error en el formato del archivo JSON."))
            raise Juego.WrongRoomFormat() from formatoincorrecto
        try:
            nombre = hashlib.md5(room.encode()).hexdigest()
            archivo = "assets/" + nombre + ".json"
            archivof = open(archivo, "x")
        except Exception:
            try:
                with open(archivo) as json_file:
                    mapa = json.load(json_file)
                    json_file.close()
                if mapa["token"] == token:
                    os.remove(archivo)
                    archivof = open(archivo, "x")
                else:
                    raise Exception    
            except Exception as mapaexistente:    
                print("Error: {}".format("El mapa ya existe."))
                raise Juego.RoomAlreadyExists() from mapaexistente

        archivof.write(roomdata)
        archivof.close()
        print("Mapa publicado.")
        return 0

    def remove(self, token, roomname, current=None):

        print("Borrando mapa")
        if not self.isvalid(token):
            print("Error: {}".format("No estas autorizado."))
            raise Juego.Unauthorized()

        try:
            nombre = hashlib.md5(roomname.encode()).hexdigest()
            archivo = "assets/" + nombre + ".json"

            with open(archivo) as json_file:
                mapa = json.load(json_file)
                json_file.close()

        except Exception as sinmapa:
            print("Error: {}".format("Mapa no encontrado."))
            raise Juego.RoomNotExists() from sinmapa

        if token != mapa["token"]:
            print("Error: {}".format("No estas autorizado."))
            raise Juego.Unauthorized()
        os.remove(archivo)
        return 0

    def isvalid(self, token):
        proxyauth = Ice.Application.communicator().stringToProxy(sys.argv[1])
        auth = Juego.AuthenticationPrx.uncheckedCast(proxyauth)

        if not auth:
            raise RuntimeError("Invalid proxy")

        return auth.isValid(token)


class Server(Ice.Application):
    def run(self, argv):

        if len(sys.argv) != 2:
            print(
                "Formato correcto: ./room_tool.py --Ice.Config=room_tool.config <proxyauth_server>"
            )
            return -1

        broker = self.communicator()
        servant = GestMapas()

        adapter = broker.createObjectAdapter("RoomServerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("RoomAdapter1"))

        print('"{}"'.format(proxy), flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
server.main(sys.argv)
sys.exit()
