#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('juego.ice')
import Juego

class Client(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        juego = Juego.ServerPrx.checkedCast(proxy)


        if not juego:
            raise RuntimeError('Invalid proxy')
        
        
        

        return 0


sys.exit(Client().main(sys.argv))