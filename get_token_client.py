#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import hashlib
import Ice
Ice.loadSlice('juego.ice')
import Juego

class Client(Ice.Application):
    def run(self, argv):

        proxy = self.communicator().stringToProxy(argv[2])
        auth = Juego.AuthenticationPrx.uncheckedCast(proxy)

        if not auth:
            raise RuntimeError('Invalid proxy')

        print("Introduce la contraseña para",argv[1])
        password = input()

        print(auth.getNewToken(argv[1],hashlib.sha256(password.encode('utf-8')).hexdigest()))

        return 0


sys.exit(Client().main(sys.argv))
