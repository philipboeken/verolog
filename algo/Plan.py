#! /usr/bin/env python
from Trip import Trip

class DayPlan:

	def __init__(self, instance):
		self.trips = []

	def addTrip(self, trip):
		self.trips.append(trip)

	def deleteTrip(self, trip):
		if trip in self.trips:
			index = self.trips.index(trip)
			del self.trips[index]

	def tripContainingNode(self, node):
		for trip in trips:
			if node in trip.nodes:
				return trip
		return False

	def concatenateTrips(self, trip1, trip2, i, j):
		s = 1
