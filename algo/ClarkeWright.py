#! /usr/bin/env python
import json
import operator
from pprint import pprint
from RoutingDay import RoutingDay
from Trip import Trip
from copy import copy

class ClarkeWright:

	def __init__(self, instance, scheduleDay):
		self.instance = instance
		self.scheduleDay = scheduleDay
		self.createSavingsList()
		self.algorithm()

	def algorithm(self):
		self.routingDay = self.initRoutingDay()
# Als je in deze def alles hieronder eruit comment is de initiele oplossing ook de eindoplossing 
		for pair, saving in self.savings:
			trip1 = self.routingDay.tripContainingRequest(pair[0], True)
			trip2 = self.routingDay.tripContainingRequest(pair[1], True)
			if trip1 and trip2:
				if not trip1.equals(trip2):
					newTrip = Trip(self.instance)
					newTrip.concatenateTrips(trip1, trip2, pair)
					if not newTrip.hasErrors(1,1):
						self.routingDay.addTrip(newTrip)
						self.routingDay.deleteTrip(trip1)
						self.routingDay.deleteTrip(trip2)

	def initRoutingDay(self):
		routingDay = RoutingDay(self.instance)
		for request in self.scheduleDay.deliveries:
			trip = Trip(self.instance, request)
			routingDay.addTrip(trip)
		for request in self.scheduleDay.pickups:
			trip = Trip(self.instance, request)
			routingDay.addTrip(trip)
		return routingDay

	def createSavingsList(self):
		self.savings = {}
		for request1 in self.scheduleDay.deliveries:
			for request2 in self.scheduleDay.deliveries:
				if not request1.equals(request2):
					if (request1,request2) not in self.savings.keys() or (request2,request1) not in self.savings.keys():
						s = self.instance.distance(0, request1.locationID) + self.instance.distance(0,request2.locationID) - self.instance.distance(request1.locationID,request2.locationID)
						self.savings[(request1,request2)] = s
			for request2 in self.scheduleDay.pickups:
				if not request1.equals(request2):
					if (request1,request2) not in self.savings.keys() or (request2,request1) not in self.savings.keys():
						s = self.instance.distance(0,request1.locationID) + self.instance.distance(0,request2.locationID) - self.instance.distance(request1.locationID,request2.locationID)
						self.savings[(request1,request2)] = s
		for request1 in self.scheduleDay.pickups:
			for request2 in self.scheduleDay.pickups:
				if not request1.equals(request2):
					if (request1,request2) not in self.savings.keys() or (request2,request1) not in self.savings.keys():
						s = self.instance.distance(0,request1.locationID) + self.instance.distance(0,request2.locationID) - self.instance.distance(request1.locationID,request2.locationID)
						self.savings[(request1,request2)] = s
		self.savings = sorted(self.savings.items(), key=operator.itemgetter(1), reverse=True)