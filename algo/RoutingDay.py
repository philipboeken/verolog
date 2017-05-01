#! /usr/bin/env python
from Trip import Trip
from copy import copy
from pprint import pprint

class RoutingDay:

	def __init__(self, instance):
		self.instance = instance
		self.trips = []
		self.costs = 0
		self.numberOfVehicles = 0

	def addTrip(self, trip):
		self.trips.append(trip)
		self.numberOfVehicles += 1

	def deleteTrip(self, trip):
		if self.contains(trip):
			index = self.trips.index(trip)
			del self.trips[index]
			self.numberOfVehicles -= 1

	def tripContainingRequest(self, request, atEnds=False):
		for trip in self.trips:
			if trip.contains(request, atEnds):
				return trip
		return False

	def distance(self):
		return sum([trip.distance() for trip in self.trips])

	def contains(self, trip):
		for trip2 in self.trips:
			if trip.equals(trip2):
				return True

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
