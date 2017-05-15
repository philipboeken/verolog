#! /usr/bin/env python
import json
from pprint import pprint
from InitSchedule import InitSchedule
from Routing import Routing
from ClarkeWright import ClarkeWright
from Solution import Solution
from TwoOpt import TwoOpt

class Strategy1:

	def __init__(self, instance):
		self.instance = instance
		self.solutionRouting = self.algorithm()
		self.solution = Solution(self.instance, self.solutionRouting)

	def algorithm(self):
		valid = False
		while not valid:
			self.initSchedule = InitSchedule(self.instance)
			routing = Routing(self.instance)
			for day, daySchedule in self.initSchedule.schedule.daySchedules.items():
				cw = ClarkeWright(self.instance, daySchedule)
				routing.addRoutingDay(day, cw.routingDay)
			valid = routing.isValid()
		return TwoOpt(self.instance, routing).routing
