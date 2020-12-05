#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# pylint: disable=C0115

"""
   ICE Publish Client
"""

import sys
import json
import Ice
Ice.loadSlice('juego.ice')
# pylint: disable=E0401
# pylint: disable=C0413
import Juego

class Client(Ice.Application):
    def run(self, argv):

        proxy = self.communicator().stringToProxy(argv[1])
        mapas = Juego.GestMapasPrx.uncheckedCast(proxy)

        if not mapas:
            raise RuntimeError('Invalid proxy')

        with open(argv[3]) as json_file:
            mapa = json.load(json_file)
            json_file.close()
        archivo = open(argv[2], "r")
        token = archivo.read()
        tokenj = {"token":token}
        mapa.update(tokenj)
        try:
            mapas.publish(token, json.dumps(mapa))
            return 0
        except Exception:
            print("Error: {}".format("Se ha producido un error."))



sys.exit(Client().main(sys.argv))
