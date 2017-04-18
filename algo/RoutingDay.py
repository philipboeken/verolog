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