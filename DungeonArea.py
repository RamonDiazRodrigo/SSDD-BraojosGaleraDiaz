
#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-
# pylint: disable=W0613
# pylint: disable=C0411
# pylint: disable=C0115
# pylint: disable=C0116

"""
   ICE Gauntlet Gestion Mapas Server
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





class DungeonArea(IceGauntlet.DungeonArea){

    def getEventChannel(){}
    def string getMap(){}
    def getActors();
        #devolver lista
    objects getItems();
    DungeonArea* getNextArea();
}