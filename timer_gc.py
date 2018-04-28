#!/usr/local/lib/python3.5
# -*- coding: utf-8 -*-
#lm280218.1604

# This file manage the timer to plot it on the beamer by node-red

import communication2gc as comm
import time
from threading import Timer

beginning = 0
dict_state = {"stop":0, "start":1, "pause":2}

def init(client):
	client.subscribe("GC_2018/timer_in")
	client.publish("GC_2018/timer_in", '{}:{:02}'.format(0, 0))

def timer(client, v_state):
	global beginning, dict_state

	if v_state.value == dict_state["stop"] and beginning != 0:
		beginning = 0
		client.publish("GC_2018/timer_in", '{}:{:02}'.format(0, 0))

		comm.init(client)

	while v_state.value == dict_state["start"]:
		time.sleep(1)
		beginning += 1

		if v_state.value == dict_state["stop"]:
			beginning = 0
			comm.init(client)

		min = int(beginning/60)
		sec = beginning%60

		client.publish("GC_2018/timer_in", '{}:{:02}'.format(min, sec))

def main_timer(v_state):
	client = comm.setup()
	init(client)

	while True:
		timer(client, v_state)
