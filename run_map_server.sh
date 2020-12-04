#!/bin/sh


PYTHON=python3

$PYTHON room_tool.py --Ice.Config=room_tool.config "$1"
PID=$!

sleep 2
kill -KILL $PID