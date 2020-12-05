#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=W1203
# pylint: disable=W0613
'''
   ICE Gauntlet Change Password Client
'''

import sys
import hashlib
import Ice
import getpass
Ice.loadSlice('juego.ice')
# pylint: disable=E0401
# pylint: disable=C0413
import Juego

class Client(Ice.Application):
    def run(self, argv):

        proxy = self.communicator().stringToProxy(argv[2])
        auth = Juego.AuthenticationPrx.uncheckedCast(proxy)

        if not auth:
            raise RuntimeError('Invalid proxy')

        print("Introduce la contraseña antigua (None si es la primera vez)")
        lastpass = input()
        while True:
            print("Introduce la contraseña nueva")
            newpass = getpass.getpass()
            print("Introduce la contraseña nueva otra vez")
            newpass2 = getpass.getpass()
            if newpass == newpass2:
                break
        if lastpass == "None":
            auth.changePassword(argv[1], None, hashlib.sha256(
                newpass.encode('utf-8')).hexdigest())
        else:
            auth.changePassword(argv[1], hashlib.sha256(lastpass.encode(
                'utf-8')).hexdigest(), hashlib.sha256(newpass.encode('utf-8')).hexdigest())

        return 0


sys.exit(Client().main(sys.argv))
