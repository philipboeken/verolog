#! /usr/bin/env python
from pprint import pprint
from Instance import Instance
import os
import json

class Solver:

	def __init__(self, instance_path = "C:\\Users\\Philip\\Documents\\School\\3BA\\Combinatorische_Optimalisatie\\verolog\\tests\\ORTEC_Test_03.txt", strategy = 'Strategy1', solution_name = "sol1metcw.txt"):
		self.instance = Instance(instance_path)
		strategy = getattr(__import__(strategy, fromlist=[strategy]), strategy)
		self.strategy = strategy(self.instance)
		self.strategy.solution.writeSolution(solution_name)
