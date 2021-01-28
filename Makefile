#!/usr/bin/make -f
# -*- mode:makefile -*-

all:

clean:
	$(RM) -r /tmp/db
	$(RM) -r /tmp/IceGauntletGame

run: clean
	$(MAKE) app-workspace
	$(MAKE) run-registry-node &
	sleep 2
	$(MAKE) run-server-node &

run-registry-node: /tmp/db/registry /tmp/db/registry-node/servers 
	icegridnode --Ice.Config=registry-node.config

run-servidor-node: /tmp/db/servidor-node/servers 
	icegridnode --Ice.Config=servidor-node.config

run-auth-node: /tmp/db/auth-node/servers 
	icegridnode --Ice.Config=auth-node.config

run-auth:
	./icegauntlet_auth_server-main/auth_server --Ice.Config=icegauntlet_auth_server-main/auth_server.conf

app-workspace: /tmp/IceGauntletGame
	cp icegauntlet.ice servidor.py /tmp/IceGauntletGame
	icepatch2calc /tmp/IceGauntletGame

/tmp/%:
	mkdir -p $@
