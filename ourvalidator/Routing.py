#! /usr/bin/env python

from RoutingDay import RoutingDay
from copy import copy

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

	def vehicleCost(self):
		return self.instance.vehicle_cost * self.maxNumberOfVehicles()

	def vehicleDayCost(self):
		return self.instance.vehicle_day_cost * self.numberOfVehicleDays()

	def distanceCost(self):
		return self.instance.distance_cost * self.distance()

	def toolCost(self):
		toolCount = self.toolCount()
		cost = 0
		for id, tool in self.instance.tools.items():
			cost += tool.cost * toolCount[id]
		return cost

	def cost(self):
		return self.vehicleCost() + self.vehicleDayCost() + self.distanceCost() + self.toolCost()

	def toolCount(self):
		depot = self.instance.startDepot
		toolCount = dict.fromkeys(depot, 0)
		for day, routingDay in self.routingDays.items():
			needed = routingDay.toolsNeeded()
			for id, tools in self.instance.tools.items():
				if self.instance.tools[id].available - (depot[id] - needed[id]) > toolCount[id]:
					toolCount[id] = self.instance.tools[id].available - (depot[id] - needed[id])
			for request in self.routingDays[day].returnDeliveries():
				depot[request.toolID] -= request.amount
			for request in self.routingDays[day].returnPickups():
				depot[request.toolID] -= request.amount	
		return toolCount

	def hasErrors(self):
		depot = {}
		errorLog = []
		for id, tool in self.instance.tools.items():
			depot[id] = tool.available
		for day, routingDay in self.routingDays.items():
			errorLog += routingDay.hasErrors(depot, day)
			for request in self.routingDays[day].returnDeliveries():
				depot[request.toolID] -= request.amount
			for request in self.routingDays[day].returnPickups():
				depot[request.toolID] -= request.amount		
		return errorLog
	
