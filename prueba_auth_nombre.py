#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# pylint: disable=C0115

"""
   ICE Get Token Client
"""
import sys
import Ice
import os
import json
import glob
import random
import hashlib
Ice.loadSlice("icegauntlet.ice")
# pylint: disable=E0401
# pylint: disable=C0413
import IceGauntlet


class Client(Ice.Application):
    def run(self, argv):

        proxy = self.communicator().stringToProxy(argv[1])
        auth = IceGauntlet.AuthenticationPrx.uncheckedCast(proxy)

        if not auth:
            raise RuntimeError("Invalid proxy")

        token = "E3EJYroaPNgnC9ZeNFJ1clksJp1OTVWyEx5Ox4mf"
        nombre = auth.getOwner(token) 
        print(nombre)
        return 0


sys.exit(Client().main(sys.argv))

