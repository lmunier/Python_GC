#!/usr/local/lib/python3.5
# -*- coding: utf-8 -*-
#lm280218.1604

# This file manage the timer to plot it on the beamer by node-red

import communication2gc as comm
import time
from threading import Timer

beginning = 0.0

def init(client):
	client.subscribe("GC_2018/timer_in")

def timer(client, v_state):
	global beginning

	if v_state.value == 0 and beginning != 0.0:
		beginning = 0.0
		client.publish("GC_2018/timer_in", str(beginning))

	while v_state.value == 1:
		time.sleep(0.1)
		beginning += 0.1

		if v_state.value == 0:
			beginning = 0.0

		client.publish("GC_2018/timer_in", str(beginning))


def main_timer(v_state):
	client = comm.setup()
	init(client)

	while True:
		timer(client, v_state)
