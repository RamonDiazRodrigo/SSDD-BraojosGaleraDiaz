#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import hashlib
import IceGauntlet
import Ice
Ice.loadSlice('icegauntlet.ice')


class Client(Ice.Application):
    def run(self, argv):

        proxy = self.communicator().stringToProxy(argv[2])
        auth = IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not auth:
            raise RuntimeError('Invalid proxy')

        print("Introduce la contraseña antigua (None si es la primera vez)")
        lastpass = input()
        while True:
            print("Introduce la contraseña nueva")
            newpass = input()
            print("Introduce la contraseña nueva otra vez")
            newpass2 = input()
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
