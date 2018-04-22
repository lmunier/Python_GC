#!/usr/local/lib/python3.5
# -*- coding: utf-8 -*-
#lm280218.1604

# This file manage the timer to plot it on the beamer by node-red

import paho.mqtt as mqtt
import paho.mqtt.client as paho

team1_point = 0
team1_passed_out = 0
team1_trash = 0

team2_point = 0
team2_passed_out = 0
team2_trash = 0

def on_connect(client, userdata, flags, rc):
	client.subscribe("GC_2018/timer_state")
	client.subscribe("GC_2018/passed-out/input/#")


def on_message(client, userdata, msg):
	global state, team1_passed_out, team2_passed_out
	strg_gc = msg.topic.split("/")
	if strg_gc[0] == "GC_2018":
		if strg_gc[1] == "passed-out":
			if strg_gc[2] == "input":
				if strg_gc[3] == "team1":
					team1_passed_out += int(str(msg.payload).split("'")[1])
				elif strg_gc[3] == "team2":
					team2_passed_out += int(str(msg.payload).split("'")[1])
				client.publish("GC_2018/passed-out/output/team1", team1_passed_out)
				client.publish("GC_2018/passed-out/output/team2", team2_passed_out)
		elif strg_gc[1] == "timer_state":
			if msg.payload == b'start':
				state.value = 1
			elif msg.payload == b'stop':
				state.value = 0
			elif msg.payload == b'pause':
				state.value = 2

def setup():
	client = paho.Client(None)
	client.connect("localhost")

	return client


def main_comm(v):
	global state
	state = v

	client = setup()

	client.on_connect = on_connect
	client.on_message = on_message

	client.loop_forever()
