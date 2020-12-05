#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# pylint: disable=C0115

"""
   ICE Get Token Client
"""

import sys
import hashlib
import Ice
import getpass
Ice.loadSlice("juego.ice")
# pylint: disable=E0401
# pylint: disable=C0413
import Juego


class Client(Ice.Application):
    def run(self, argv):

        proxy = self.communicator().stringToProxy(argv[2])
        auth = Juego.AuthenticationPrx.uncheckedCast(proxy)

        if not auth:
            raise RuntimeError("Invalid proxy")

        password = getpass.getpass("Introduce la contrasena: ")
        archivo = open("token.txt", "w")
        archivo.write(
            auth.getNewToken(
                argv[1], hashlib.sha256(password.encode("utf-8")).hexdigest()
            )
        )
        archivo.close()
        return 0


sys.exit(Client().main(sys.argv))
