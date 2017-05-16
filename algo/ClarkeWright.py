#! /usr/bin/env python
import operator
from RoutingDay import RoutingDay
from Trip import Trip

class ClarkeWright:
	def __init__(self, instance, scheduleDay):
		self.instance = instance
		self.scheduleDay = scheduleDay
		self.inventory = scheduleDay.inventory
		self.createSavingsList()
		self.algorithm()

	def algorithm(self):
		self.routingDay = self.initRoutingDay()
		for pair, saving in self.savings:
			trip1 = self.routingDay.tripContainingRequest(pair[0], True)
			trip2 = self.routingDay.tripContainingRequest(pair[1], True)
			if trip1 and trip2:
				if not trip1.equals(trip2):
					newTrip = Trip(self.instance)
					newTrip.concatenateTrips(trip2, trip1, pair)
					if newTrip.isValid():
						validChange = True
						benefit = True
						for toolID, tool in self.instance.tools.items():
							if self.inventory[toolID] < 0:
								benefit = False
						newInventory  = newTrip.inventoryChange()
						inventory1 = trip1.inventoryChange()
						inventory2 = trip2.inventoryChange()
						for toolID, tool in self.instance.tools.items():
							change = newInventory[toolID] - inventory1[toolID] - inventory2[toolID]
							if change < 0 and self.inventory[toolID] + change < 0:
								validChange = False
								break
							if self.inventory[toolID] < 0 and change > 0:
								benefit = True		
						if validChange and benefit:
							self.routingDay.addTrip(newTrip)
							self.routingDay.deleteTrip(trip1)
							self.routingDay.deleteTrip(trip2)
							for toolID, tool in self.instance.tools.items():
								change = newInventory[toolID] - inventory1[toolID] - inventory2[toolID]
								self.inventory[toolID] = self.inventory[toolID] + change

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
					if (request1, request2) not in self.savings.keys() or (request2, request1) not in self.savings.keys():
						s = self.instance.distance(0, request1.locationID) + self.instance.distance(0, request2.locationID) - self.instance.distance(request1.locationID, request2.locationID)
						self.savings[(request1,request2)] = s
			for request2 in self.scheduleDay.pickups:
				if not request1.equals(request2):
					if (request1,request2) not in self.savings.keys() or (request2,request1) not in self.savings.keys():
						s = self.instance.distance(0, request1.locationID) + self.instance.distance(0, request2.locationID) - self.instance.distance(request1.locationID, request2.locationID)
						self.savings[(request1,request2)] = s
		for request1 in self.scheduleDay.pickups:
			for request2 in self.scheduleDay.pickups:
				if not request1.equals(request2):
					if (request1,request2) not in self.savings.keys() or (request2,request1) not in self.savings.keys():
						s = self.instance.distance(0, request1.locationID) + self.instance.distance(0, request2.locationID) - self.instance.distance(request1.locationID, request2.locationID)
						self.savings[(request1,request2)] = s
		self.savings = sorted(self.savings.items(), key=operator.itemgetter(1), reverse=True)
		