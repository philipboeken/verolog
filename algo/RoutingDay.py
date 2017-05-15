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
	
	def mergeLoop(self):
		for trip1 in self.trips:
				for trip2 in self.trips:
					if trip1.dist() + trip2.dist() <= self.instance.max_trip_distance and trip1 != trip2:
						trip1.addRoute(trip2)
						self.deleteTrip(trip2)
						return True
		return False

	def mergeTrips(self): 
		nextLoop = True
		while nextLoop:
			nextLoop = self.mergeLoop()
		self.numberOfVehicles = len(self.trips)

	def distance(self):
		return sum([trip.dist() for trip in self.trips])

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

	def isValid(self, startDepot):
		for id, amount in self.toolsNeeded().items():
			if startDepot[id] - amount < 0:
				return False
		return True