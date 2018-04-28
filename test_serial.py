#!/usr/local/lib/python3.5
# -*- coding: utf-8 -*-
#lm280418.1130

# This file test la communication serial

import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
ser.write('x')
