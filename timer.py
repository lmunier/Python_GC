#!/usr/local/lib/python3.5
# -*- coding: utf-8 -*-
#lm280218.1604

# This file manage the timer to plot it on the beamer by node-red

import communication2gc as comm
import time
from threading import Timer

beginning = 0.00

def init(client):
	client.subscribe("GC_2018/timer_in")

def timer(client, v_state):
	global beginning

	if v_state.value == 0 and beginning != 0.0:
		beginning = 0.00
		client.publish("GC_2018/timer_in", '{}:{:02}.{:02}'.format(0, 0, 0))

	while v_state.value == 1:
		time.sleep(0.01)
		beginning += 0.01

		if v_state.value == 0:
			beginning = 0.00

		min = int(beginning/60)
		sec = int(beginning%60)
		milli = int((beginning - int(beginning))*100)

		client.publish("GC_2018/timer_in", '{}:{:02}.{:02}'.format(min, sec, milli))

def main_timer(v_state):
	client = comm.setup()
	init(client)

	while True:
		timer(client, v_state)
