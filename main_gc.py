#!/usr/local/lib/python3.5
# -*- coding: utf-8 -*-
#lm220418.1449

# This file manage all the python file for the gc 2018

import communication2gc as comm
import timer
import multiprocessing


if __name__ == '__main__':
	v = multiprocessing.Value('i', 0)

	p1 = multiprocessing.Process(target=comm.main_comm, args = (v,))
	p1.start()
	p2 = multiprocessing.Process(target=timer.main_timer, args = (v,))
	p2.start()
	p1.join()
	p2.join()
