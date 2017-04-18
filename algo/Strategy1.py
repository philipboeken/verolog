#! /usr/bin/env python
import json
from pprint import pprint
from InitSchedule import InitSchedule
from Routing import Routing
from ClarkeWright import ClarkeWright
from Solution import Solution

class Strategy1:

	def __init__(self, instance):
		self.instance = instance
		self.solutionRouting = self.algorithm()
		self.solution = Solution(self.instance, self.solutionRouting)

	def algorithm(self):
		routing = Routing()
		self.initSchedule = InitSchedule(self.instance)
		for day, daySchedule in self.initSchedule.schedule.daySchedules.items():
			cw = ClarkeWright(self.instance, daySchedule)
			routing.addRoutingDay(day, cw.routingDay)
		return routing
