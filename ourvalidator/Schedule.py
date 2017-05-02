#! /usr/bin/env python

from copy import copy
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

	def addDeliveryOnDay(self, day, request):
		self.scheduleDays[day].addDelivery(copy(request))

	def addPickupOnDay(self, day, request):
		self.scheduleDays[day].addPickup(copy(request))

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
		doubleDelivery = set([x for x in allDeliveries if allDeliveries.count(x) > 1])
		doublePickups = set([x for x in allPickups if allPickups.count(x) > 1])
		if doubleDelivery:
			errorLog.append('Delivery done twice: ' + ', '.join(str(r) for r in list(doubleDelivery)))
		if doublePickups:
			errorLog.append('Pickup done twice: ' + ', '.join(str(r) for r in list(doublePickups)))
		notPickedUp = list(set(allRequests) - set(allPickups))
		notDelivered = list(set(allRequests) - set(allDeliveries))
		for day, scheduleDay in self.scheduleDays.items():
			for request in self.scheduleDays[day].deliveries:
				deliveryID = request.id
				if not request.firstDay <= day <= request.lastDay: # of elke delivery wel in de goede timespan gebeurt
					errorLog.append('Day: ' + str(day) + ' Request: ' + str(request.id) + ' Error: Delivery not done within correct timespan')
				try:
					if deliveryID not in [-x.id for x in self.scheduleDays[day + request.daysStay].pickups] and deliveryID in allPickups: # of elke tool die wordt gedelivered ook op de goede dag wordt opgehaald
						errorLog.append('Day: ' + str(day) + ' Request: ' + str(request.id) + ' Error: Pickup not done on the right day')
				except:
					errorLog.append('Request is not picked up: ' + str(deliveryID))
		if notDelivered: # of alle requests worden delivered
			errorLog.append('The following requests have not been delivered: ' + ', '.join(str(r) for r in notDelivered)) 
		if notPickedUp: # of alle requests worden opgehaald
			errorLog.append('The following requests have not been picked up: ' + ', '.join(str(r) for r in list(notPickedUp)))
		return errorLog
