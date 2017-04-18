#! /usr/bin/env python
from RoutingDay import RoutingDay

class Routing:

	def __init__(self, instance):
		self.instance = instance
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
		
	def isValid(self):
		depot = {}
		for id, tool in self.instance.tools.items():
			depot[id] = 0
		for day, routingDay in self.routingDays.items():
			if !routingDay.isValid(depot):
				return False
			for id, change in routingDay.changeInDepot():
				depot[id] += change
		return True
		