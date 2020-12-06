#!/bin/sh


PYTHON=python3

$PYTHON server_game.py --Ice.Config=server_game.config
PID=$!

sleep 2
kill -KILL $PID