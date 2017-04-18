#! /usr/bin/env python
from RoutingDay import RoutingDay

class Routing:

	def __init__(self):
		self.routingDays = {}

	def addRoutingDay(self, day, routingDay):
		self.routingDays[day] = routingDay

	def maxNumberOfVehicles(self):
		max = 0
		for day, routingDay in self.routingDays.items():
			max = routingDay.numberOfVehicles if routingDay.numberOfVehicles > max else max
		return max

	def numberOfVehicleDays(self):
		return sum([routingDay.numberOfVehicles for day, routingDay in self.routingDays.items()])

	def distance(self):
		return sum([routingDay.distance() for day, routingDay in self.routingDays.items()])