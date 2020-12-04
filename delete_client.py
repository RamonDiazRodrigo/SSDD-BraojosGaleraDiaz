#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import hashlib
import json
import Ice
Ice.loadSlice('juego.ice')
import Juego

class Client(Ice.Application):
    def run(self, argv):
        print("proxy mapa:"+argv[1])
        proxy = self.communicator().stringToProxy(argv[1])
        mapas = Juego.GestMapasPrx.uncheckedCast(proxy)

        if not mapas:
            raise RuntimeError('Invalid proxy')
            
        f = open(argv[2], "r")
        token = f.read()
      
        mapas.remove(token, argv[3]) # para borrar mapa
        return 0


sys.exit(Client().main(sys.argv))
