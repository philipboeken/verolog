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

	# Hierin zit een schedulingprobleem: meerdere korte trips, hoe deze onderverdelen 
	# onder vehicles om zo weinig mogelijk vehicles te gebruiken
	def mergeTrips(self): 
		for trip1 in self.trips:
			for trip2 in self.trips:
				if trip1.distance + trip2.distance <= self.instance.max_trip_distance:
					trip1.addTrip(trip2)
					self.deleteTrip(trip2)
		self.numberOfVehicles = len(self.trips)

	def distance(self):
		return sum([trip.distance for trip in self.trips])

	def contains(self, trip):
		for trip2 in self.trips:
			if trip.equals(trip2):
				return True

	def changeInDepot(self):
		change = {}
		for id, amount in startDepot.items():
            change[id] = 0
		for id, amount in self.toolsNeeded().items():
			change[id] -= amount
		for id, amount in self.toolsRetrieved().items():
			change[id] -= amount

	def toolsNeeded(self):
		toolsNeeded = {}
		for id, tool in self.instance.tools.items():
			toolsNeeded[id] = 0
		for trip in trips:
			for id, amount in trip.toolsNeeded().items():
				toolsNeeded[id] += amount
		return toolsNeeded

	def toolsRetrieved(self):
		toolsRetrieved = {}
		for id, tool in self.instance.tools.items():
			toolsRetrieved[id] = 0
		for trip in trips:
			for id, amount in trip.toolsRetrieved().items():
				toolsRetrieved[id] += amount
		return toolsRetrieved

# Check gegeven een depot aan het begin van de dag of de vereisten van de trips niet groter zijn dan het depot
	def isValid(self, startDepot):
		for id, amount in self.toolsNeeded():
			if startDepot[id] < amount:
				return False
		for trip in trips:
			if !trip.isValid():
				return False
		return True
