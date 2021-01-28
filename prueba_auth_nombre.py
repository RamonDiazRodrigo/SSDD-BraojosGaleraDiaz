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
        nombre = "No autorizado"
        token = "3tcFgqEmwhFxl0tIdPJShDPrkX2EClervKIhm3F"
        try:
            nombre = auth.getOwner(token) 
        except Exception as identifier:
            raise IceGauntlet.Unauthorized from identifier
        
        print(nombre)
        return 0


sys.exit(Client().main(sys.argv))

