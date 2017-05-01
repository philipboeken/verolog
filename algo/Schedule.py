#! /usr/bin/env python
from copy import copy
from pprint import pprint
from ScheduleDay import ScheduleDay

class Schedule:

	def __init__(self, instance):
		self.instance = instance
		self.days = instance.days
		self.scheduleDays = {}
		for day in range(1, self.days + 1):
			self.scheduleDays[day] = ScheduleDay()

	def __str__(self):
		s = ''
		for day, scheduleDay in self.scheduleDays.items():
			s += str(day) + ': \n' + str(scheduleDay)
		return s

	def addDeliveryOnDay(self, day, request, planPickup=True):
		self.scheduleDays[day].addDelivery(copy(request))
		if planPickup:
			self.scheduleDays[day + request.daysStay].addPickup(copy(request))

	def addPickupOnDay(self, day, request):
		self.scheduleDays[day].addPickup(copy(request))

	def deleteDelivery(self, request):
		for day, scheduleDay in self.scheduleDays.items():
			if scheduleDay.deleteDelivery(request):
				self.scheduleDays[day + request.daysStay].deletePickup(copy(request))
				return True
		return False

	def isFeasible(self):
		errorLog = []
		requests = self.instance.requests
		depot = {}
		for toolID, tool in self.instance.tools.items():
			depot[toolID] = tool.available
		for day, scheduleDay in self.scheduleDays.items():
			for request in self.scheduleDays[day].deliveries:
				depot[request.toolID] -= request.amount
			for request in self.scheduleDays[day].pickups:
				depot[request.toolID] -= request.amount
			for toolID, tool in self.instance.tools.items():
				if depot[toolID] < 0:
					return False
		return True

	def allPickups(self):
		allPickups = []
		for day, scheduleDay in self.scheduleDays.items():
			allPickups += scheduleDay.pickups
		return allPickups

	def allDeliveries(self):
		allDeliveries = []
		for day, scheduleDay in self.scheduleDays.items():
			allDeliveries += scheduleDay.deliveries
		return allDeliveries

	def hasErrors(self):
		errorLog = []
		allPickups = [-p.id for p in self.allPickups()]
		allDeliveries = [d.id for d in self.allDeliveries()]
		allRequests = [r for r in self.instance.requests]
		notPickedUp = list(set(allRequests) - set(allPickups))
		notDelivered = list(set(allRequests) - set(allDeliveries))
		for day, scheduleDay in self.scheduleDays.items():
			for request in self.scheduleDays[day].deliveries:
				deliveryID = request.id
				if not request.firstDay <= day <= request.lastDay: # of elke delivery wel in de goede timespan gebeurt
					errorLog.append('Day: ' + str(day) + ' Request: ' + str(request) + ' Error: Delivery not done within correct timespan')
				if deliveryID not in [-x.id for x in self.scheduleDays[day + request.daysStay].pickups] and deliveryID in allPickups: # of elke tool die wordt gedelivered ook op de goede dag wordt opgehaald
					errorLog.append('Day: ' + str(day) + ' Request: ' + str(request) + ' Error: Pickup not done on the right day')
		if notDelivered: # of alle requests worden delivered
			errorLog.append('The following requests have not been delivered: ' + ', '.join(str(r) for r in notDelivered)) 
		if notPickedUp: # of alle requests worden opgehaald
			errorLog.append('The following requests have not been picked up: ' + ', '.join(str(r) for r in list(notPickedUp)))
		return errorLog

	def test(self):
		errorLog = []
		requests = self.instance.requests
		toDeliver = list(copy(requests).keys())
		deliveries = {}
		depot = {}
		for toolID, tool in self.instance.tools.items():
			depot[toolID] = tool.available
		for day, scheduleDay in self.scheduleDays.items():
			for request in self.scheduleDays[day].deliveries:
				depot[request.toolID] -= request.amount
			print(depot[1]) # of de voorraad van alle tools altijd >= 0 is
			for request in self.scheduleDays[day].pickups:
				depot[request.toolID] -= request.amount
			print(depot[1]) # of de voorraad van alle tools altijd >= 0 is

	def amount(self):
		sum = 0
		for request in self.scheduleDays:
			sum += self.scheduleDays[request].amount()
		return sum

	def inv(self):
		depot = {}
		minimum=100
		requests = self.instance.requests
		depot = {}
		for toolID, tool in self.instance.tools.items():
			depot[toolID] = tool.available
		for day, scheduleDay in self.scheduleDays.items():
			for request in self.scheduleDays[day].deliveries:
				depot[request.toolID] -= request.amount
			for request in self.scheduleDays[day].pickups:
				depot[request.toolID] -= request.amount
			for toolID, tool in self.instance.tools.items():
				if depot[toolID] < minimum:
					minimum = depot[toolID]
		return minimum