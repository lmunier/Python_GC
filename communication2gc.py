#!/usr/local/lib/python3.5
# -*- coding: utf-8 -*-
#lm280218.1604

# This file manage the timer to plot it on the beamer by node-red

import multiprocessing
import paho.mqtt as mqtt
import paho.mqtt.client as paho
import timer_gc

state = multiprocessing.Value('i', 0)

team1_name = ""
team1_recipes = ""
team1_point = 0
team1_passed_out = 0
team1_trash = 0
team1_good_recipes = 0
team1_good_ingredient = 0

team2_name = ""
team2_recipes = ""
team2_point = 0
team2_passed_out = 0
team2_trash = 0
team2_good_recipes = 0
team2_good_ingredient = 0

round = 0
global_recipes = ""
match = ""

def on_connect(client, userdata, flags, rc):
	# Subscribing
	client.subscribe("GC_2018/timer_state")
	client.subscribe("GC_2018/passed-out/input/#")
	client.subscribe("GC_2018/round/input/#")
	client.subscribe("GC_2018/recipes/input/#")
	client.subscribe("GC_2018/trash/input/#")
	client.subscribe("GC_2018/save")
	client.subscribe("GC_2018/match/input")

	init(client)

def on_message(client, userdata, msg):
	global state, round, global_recipes, dict_state, match
	global team1_name, team1_good_ingredient, team1_passed_out, team1_trash, team1_recipes, team1_good_recipes, team1_point
	global team2_name, team2_good_ingredient, team2_passed_out, team2_trash, team2_recipes, team2_good_recipes, team2_point

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
				print("Passed-out for team1 " +str(team1_passed_out)+" and for team2 "+str(team2_passed_out))

		elif strg_gc[1] == "trash":
			if strg_gc[2] == "input":
				if strg_gc[3] == "team1":
					team1_trash += int(str(msg.payload).split("'")[1])
				elif strg_gc[3] == "team2":
					team2_trash += int(str(msg.payload).split("'")[1])

				client.publish("GC_2018/trash/output/team1", team1_trash)
				client.publish("GC_2018/trash/output/team2", team2_trash)
				print("Trash for team1 " +str(team1_trash)+" and for team2 "+str(team2_trash))

		elif strg_gc[1] == "timer_state":
			if msg.payload == b'start':
				state.value = timer_gc.dict_state["start"]
			elif msg.payload == b'stop':
				state.value = timer_gc.dict_state["stop"]
			elif msg.payload == b'pause':
				state.value = timer_gc.dict_state["pause"]

		elif strg_gc[1] == "round":
			if strg_gc[2] == "input":
				if strg_gc[3] == "global":
					round = int(str(msg.payload).split("'")[1])
					print("Round " +str(round)+" is live")

		elif strg_gc[1] == "recipes":
			if strg_gc[2] == "input":
				if strg_gc[3] == "team1":
					msgpayload1 = (str(msg.payload).split("'")[1]).split("-")
					team1_recipes = msgpayload1[0]
					team1_good_recipes = int(msgpayload1[2])
					if (len(msgpayload1) >3):
						team1_good_ingredient = int(msgpayload1[3])
					print("Team1 current recipes is " + team1_recipes)
				elif strg_gc[3] == "team2":
					msgpayload2 = (str(msg.payload).split("'")[1]).split("-")
					team2_recipes = msgpayload2[0]
					team2_good_recipes = int(msgpayload2[2])
					if (len(msgpayload2) >3):
						team2_good_ingredient = int(msgpayload2[3])
					print("Team2 current recipes is " + team2_recipes)
				elif strg_gc[3] == "global":
					global_recipes = str(msg.payload).split("'")[1]
					print("Current recipes is " + global_recipes)
		elif strg_gc[1] == "name":
			if strg_gc[2] == "input":
				if strg_gc[3] == "team1":
					team1_name = (str(msg.payload).split("'")[1])
				elif strg_gc[3] == "team2":
					team2_name = (str(msg.payload).split("'")[1])

		elif strg_gc[1] == "save":
			file = open("/home/pi/Documents/GC_save/matchsave"+match+".txt","w")
			file.write("MANUAL SAVE :\r\nGlobal recipes: "+global_recipes+"\r\n")
			file.write("Team 1: "+team1_name+"\r\nPoints: "+str(team2_point)+"\r\nRecipes"+team1_recipes+"\r\nNombre dans poubelle "+str(team1_trash)+"\r\nNombre de périmé pas dans poubelle"+str(team1_passed_out)+"\r\n")
			file.write("\r\nTeam 2: "+team2_name+"\r\nPoint: "+str(team2_point)+"\r\nRecipes: "+team2_recipes+"\r\nNombre dans poubelle "+str(team2_trash)+"\r\nNombre de périmé pas dans poubelle"+str(team2_passed_out)+"\r\n")
			file.close()
			print("SAVE to the file: matchsave"+match+".txt")
		elif strg_gc[1] == "match":
			if strg_gc[2] == "input":
				match = str(msg.payload).split("'")[1]

	team1_point = team1_passed_out*(-2) + team1_trash + team1_good_recipes*(round+1)+ team1_good_ingredient
	team2_point = team2_passed_out*(-2) + team2_trash + team2_good_recipes*(round+1)+ team2_good_ingredient
	print("Team1 " +str(team1_point)+"      Team2 "+str(team2_point))

	client.publish("GC_2018/point/output/team1", team1_point)
	client.publish("GC_2018/point/output/team2", team2_point)
	
	file = open("/home/pi/Documents/GC_save/matchsave"+match+".txt","w")
	file.write("Automatic SAVE :\r\nGlobal recipes: "+global_recipes+"\r\n")
	file.write("Team 1: "+team1_name+"\r\nPoints: "+str(team2_point)+"\r\nRecipes"+team1_recipes+"\r\nNombre dans poubelle "+str(team1_trash)+"\r\nNombre de périmé pas dans poubelle"+str(team1_passed_out)+"\r\n")
	file.write("\r\nTeam 2: "+team2_name+"\r\nPoint: "+str(team2_point)+"\r\nRecipes: "+team2_recipes+"\r\nNombre dans poubelle "+str(team2_trash)+"\r\nNombre de périmé pas dans poubelle"+str(team2_passed_out)+"\r\n")
	file.close()
	print("SAVE to the file: matchsave"+match+".txt")


def setup():
	client = paho.Client(None)
	client.connect("localhost")

	return client


def init(client):
	global state, round, global_recipes, dict_state
	global team1_passed_out, team1_trash, team1_recipes, team1_good_recipes, team1_point
	global team2_passed_out, team2_trash, team2_recipes, team2_good_recipes, team2_point

	state.value = timer_gc.dict_state["stop"]
	global_recipes = ""

	team1_passed_out = 0
	team1_trash = 0
	team1_recipes = ""
	team1_good_recipes = 0
	team1_point = 0

	team2_passed_out = 0
	team2_trash = 0
	team2_recipes = ""
	team2_good_recipes = 0
	team2_point = 0

	client.publish("GC_2018/passed-out/output/team1", team1_passed_out)
	client.publish("GC_2018/trash/output/team1", team1_trash)
	client.publish("GC_2018/point/output/team1", team1_point)

	client.publish("GC_2018/passed-out/output/team2", team2_passed_out)
	client.publish("GC_2018/trash/output/team2", team2_trash)
	client.publish("GC_2018/point/output/team2", team2_point)


def main_comm(v):
	global state
	state = v

	client = setup()
	init(client)

	client.on_connect = on_connect
	client.on_message = on_message

	client.loop_forever()
