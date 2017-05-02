#! /usr/bin/env python

from Trip import Trip
from copy import copy

class RoutingDay:

	def __init__(self, instance):
		self.instance = instance
		self.trips = []
		self.costs = 0
		self.numberOfVehicles = 0

	def addTrip(self, trip):
		self.trips.append(trip)
		self.numberOfVehicles += 1

	def distance(self):
		return sum([trip.distance() for trip in self.trips])

	def toolsNeeded(self):
		tools = {}
		for id, tool in self.instance.tools.items():
			tools[id] = 0
		for trip in self.trips:
			for id, amount in trip.totalToolsNeeded().items():
				tools[id] += amount
		return tools

	def hasErrors(self, startDepot, day):
		errorLog = []
		for id, amount in self.toolsNeeded().items():
			errorLog += ['Negative depot for tool ' + str(id) + ' on day ' + str(day)] if startDepot[id] - amount < 0 else []
		for i in range(len(self.trips)):
			errorLog += self.trips[i].hasErrors(day, i+1)
		return errorLog

	def returnDeliveries(self):
		deliveries = []
		for trip in self.trips:
			deliveries += trip.returnDeliveries()
		return deliveries

	def returnPickups(self):
		pickups = []
		for trip in self.trips:
			pickups += trip.returnPickups()
		return pickups
