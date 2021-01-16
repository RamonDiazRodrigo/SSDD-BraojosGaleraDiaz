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

class RoomManagerSync(IceGauntlet.RoomManagerSync):
    
    def __init__(self, server, other):
        self.serverMaster = server
        self.serverRoom = other
    
    def hello(self, manager, managerId, current=None):
        if manager!=self.serverRoom:
            print("New serverRoom: ", manager)
            self.serverMaster.serverList.append(manager)
            manager.announce(IceGauntlet.RoomManagerPrx.checkedCast(self.serverRoom))
            
            publisherUpdate = self.serverMaster.topicUpdate.getPublisher()
            managerUpdate = IceGauntlet.RoomManagerSyncPrx.uncheckedCast(publisherUpdate)
            filesDict = self.serverMaster.files
            fileList = self.serverMaster.dictToList(filesDict)
            for file in fileList:
                managerUpdate.newFile(file)

    def announce(self, manager, managerId, current=None):
        self.serverMaster.serverList.append(manager)
        print('Previous Manager: ', managerId)

class RoomManager(IceGauntlet.RoomManager):
    
    def __init__(self, server):
        self.serverMaster = server

    def getRoom(self, current=None):

        try:
            rooms = []
            for name in glob.glob('assets/*.json'):
                rooms.append(name)
            if "assets/palette.json" in rooms:
                rooms.remove("assets/palette.json")
            rng = random.randint(0, len(rooms)-1)
            return rooms[rng]
        except Exception as noexiste:
            print("Error: {}".format("Mapa no encontrado."))
            raise IceGauntlet.RoomNotExists() from noexiste

    def publish(self, token, roomdata, current=None):

        print("Publicando mapa...")
        if not self.isvalid(token):
            print("Error: {}".format("No estas autorizado."))
            raise IceGauntlet.Unauthorized()

        try:
            roomdatajson = json.loads(roomdata)
            room = roomdatajson["room"]
            _data = roomdatajson["data"]
        except Exception as formatoincorrecto:
            print("Error: {}".format("Error en el formato del archivo JSON."))
            raise IceGauntlet.WrongRoomFormat() from formatoincorrecto
        try:
            nombre = hashlib.md5(room.encode()).hexdigest()
            archivo = "assets/" + nombre + ".json"
            archivof = open(archivo, "x")
        except Exception:
            try:
                with open(archivo) as json_file:
                    mapa = json.load(json_file)
                    json_file.close()
                if mapa["token"] == token:
                    os.remove(archivo)
                    archivof = open(archivo, "x")
                else:
                    raise Exception
            except Exception as mapaexistente:
                print("Error: {}".format("El mapa ya existe."))
                raise IceGauntlet.RoomAlreadyExists() from mapaexistente

        archivof.write(roomdata)
        archivof.close()
        print("Mapa publicado.")
        return 0

    def remove(self, token, roomname, current=None):

        print("Borrando mapa")
        if not self.isvalid(token):
            print("Error: {}".format("No estas autorizado."))
            raise IceGauntlet.Unauthorized()

        try:
            nombre = hashlib.md5(roomname.encode()).hexdigest()
            archivo = "assets/" + nombre + ".json"

            with open(archivo) as json_file:
                mapa = json.load(json_file)
                json_file.close()

        except Exception as sinmapa:
            print("Error: {}".format("Mapa no encontrado."))
            raise IceGauntlet.RoomNotExists() from sinmapa

        if token != mapa["token"]:
            print("Error: {}".format("No estas autorizado."))
            raise IceGauntlet.Unauthorized()
        os.remove(archivo)
        return 0

    def availableRooms(self, current=None):
        rooms = self.serverMaster.serverList
        return self.serverMaster.dictToList(rooms)

    def isvalid(self, token):
        proxyauth = Ice.Application.communicator().stringToProxy(sys.argv[1])
        auth = IceGauntlet.AuthenticationPrx.uncheckedCast(proxyauth)

        if not auth:
            raise RuntimeError("Invalid proxy")

        return auth.isValid(token)


class Server(Ice.Application):
    rooms = {}
    serverList = []
    topicUpdate = None

    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        pr = self.communicator().propertyToProxy(key)
        if pr is None:
            print("property {} not set".format(key))
            return None

        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(pr)

    def run(self, argv):

        if len(sys.argv) != 2:
            print(
                "Formato correcto: ./room_tool.py --Ice.Config=room_tool.config <proxyauth_server>"
            )
            return -1

        broker = self.communicator()
        servant = RoomManager(self)

        adapter = broker.createObjectAdapter("ServerAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("ServerAdapter1"))
        
        print('"{}"'.format(proxy), flush=True)

        self.serverList.append(proxy)
        
        #####
        
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            print('Invalid proxy')
            return 2

        ###SUBSCRIBER SYNC###
        
        helloServant = RoomManagerSync(self, proxy)
        indirect_subscriber = adapter.addWithUUID(helloServant)
        object_identity = indirect_subscriber.ice_getIdentity()
        subscriber = adapter.createDirectProxy(object_identity)
        topic_name = "RoomManagerSyncChannel"
        qos = {}
        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_mgr.create(topic_name)
        topic.subscribeAndGetPublisher(qos, subscriber)
        print("Waiting new events in RoomManagerSyncChannel...")
        
        adapter.activate()
        
        ###PUBLISHER SYNC###
        
        publisher = topic.getPublisher()
        mRoom = IceGauntlet.RoomManagerSyncPrx.uncheckedCast(publisher)
        mRoom.hello(IceGauntlet.RoomManagerPrx.checkedCast(proxy))
        
        #####
        
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        topic.unsubscribe(subscriber)

        return 0


server = Server()
server.main(sys.argv)
sys.exit()
