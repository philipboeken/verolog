#! /usr/bin/env python
import sys
from Instance import Instance
from ScheduleMaker import ScheduleMaker
from Routing import Routing
from ClarkeWright import ClarkeWright
from Solution import Solution
from TwoOpt import TwoOpt

def algorithm(instance):
	valid = False
	while not valid:
		initSchedule = ScheduleMaker(instance)
		routing = Routing(instance)
		for day, scheduleDay in initSchedule.schedule.scheduleDays.items():
			cw = ClarkeWright(instance, scheduleDay)
			routing.addRoutingDay(day, cw.routingDay)
		valid = routing.isValid()
	return TwoOpt(instance, routing).routing

if __name__ == "__main__":
	args = sys.argv
	instance = Instance(args[1])
	solutionRouting = algorithm(instance)
	solution = Solution(instance, solutionRouting)
	solution.writeSolution(args[2])
