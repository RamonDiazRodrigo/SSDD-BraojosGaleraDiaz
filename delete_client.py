#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=C0115

'''
   ICE Gauntlet Delete Client
'''

import sys
import Ice
Ice.loadSlice('juego.ice')
# pylint: disable=E0401
# pylint: disable=C0413
import Juego

class Client(Ice.Application):
    def run(self, argv):
        print("proxy mapa:"+argv[1])
        proxy = self.communicator().stringToProxy(argv[1])
        mapas = Juego.GestMapasPrx.uncheckedCast(proxy)

        if not mapas:
            raise RuntimeError('Invalid proxy')

        archivo = open(argv[2], "r")
        token = archivo.read()

        mapas.remove(token, argv[3])
        return 0


sys.exit(Client().main(sys.argv))
