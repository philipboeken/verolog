#! /usr/bin/env python
from copy import copy
from pprint import pprint
from DaySchedule import DaySchedule

class Schedule:

	def __init__(self, instance):
		self.instance = instance
		self.days = instance.days
		self.daySchedules = {}
		for day in range(1, self.days + 1):
			self.daySchedules[day] = DaySchedule()

	def addDeliveryOnDay(self, day, request):
		self.daySchedules[day].addDelivery(request)
		self.daySchedules[day + request.daysStay].addPickup(copy(request))

	def deleteDelivery(self, request):
		for day, daySchedule in self.daySchedules.items():
			if daySchedule.deleteDelivery(request):
				self.daySchedules[day + request.daysStay].deletePickup(copy(request))
				return True
		return False

	# Checkt:
		# - of elke delivery wel in de goede timespan gebeurt
		# - of elke tool die wordt gedelivered ook op de goede dag wordt opgehaald
		# - of de voorraad van alle tools altijd >= 0 is
		# - of elke pickup wel eerst is delivered
		# - of alle tools die zijn gedelivered ook worden opgehaald
		# - of alle requests afgehandeld worden	
	def isValidShort(self):
		errorLog = []
		requests = self.instance.requests
		depot = {}
		for toolID, tool in self.instance.tools.items():
			depot[toolID] = tool.available
		for day, daySchedule in self.daySchedules.items():
			for request in self.daySchedules[day].deliveries:
				depot[request.toolID] -= request.amount
				for toolID, tool in self.instance.tools.items():
					if depot[toolID] < 0:
						return False
			for request in self.daySchedules[day].pickups:
				depot[request.toolID] -= request.amount
		return True

	def isValid(self):
		errorLog = []
		requests = self.instance.requests
		toDeliver = list(copy(requests).keys())
		deliveries = {}
		depot = {}
		for toolID, tool in self.instance.tools.items():
			depot[toolID] = tool.available
		for day, daySchedule in self.daySchedules.items():
			for request in self.daySchedules[day].deliveries:
				deliveryID = request.id
				del toDeliver[toDeliver.index(deliveryID)]
				deliveries[deliveryID] = request
				#depot[request.toolID] -= request.amount
				if not request.firstDay <= day <= request.lastDay: # of elke delivery wel in de goede timespan gebeurt
					errorLog.append('Day: ' + str(day) + ' Request: ' + request.toString() + ' Error: Delivery not done within correct timespan')
				if deliveryID not in [-x.id for x in self.daySchedules[day + request.daysStay].pickups]: # of elke tool die wordt gedelivered ook op de goede dag wordt opgehaald
					errorLog.append('Day: ' + str(day) + ' Request: ' + request.toString() + ' Error: Pickup not done on the right day')
				if depot[request.toolID] < 0: # of de voorraad van alle tools altijd >= 0 is
					errorLog.append('Day: ' + str(day) + ' Request: ' + request.toString() + ' Error: Negative depot.' ) 
			for request in self.daySchedules[day].pickups:
				pickupID = request.id
				if -pickupID not in deliveries.keys(): # of elke pickup wel eerst is delivered
					errorLog.append('Day: ' + str(day) + ' Request: ' + request.toString() + ' Error: Pickup is not delivered first.' ) 
				else:
					del deliveries[-pickupID]
				depot[request.toolID] += request.amount
		if deliveries: # of alle tools die zijn gedelivered ook worden opgehaald
			errorLog.append('Day: ' + str(day) + ' Error: A delivery deliveries is not picked up.' ) 
		if toDeliver: # of alle requests afgehandeld worden
			errorLog.append('Day: ' + str(day) + ' Error: Not all requests are delivered.' ) 
		if errorLog:
			pprint(errorLog)
			return False
		else:
			return True

	def test(self):
		errorLog = []
		requests = self.instance.requests
		toDeliver = list(copy(requests).keys())
		deliveries = {}
		depot = {}
		for toolID, tool in self.instance.tools.items():
			depot[toolID] = tool.available
		for day, daySchedule in self.daySchedules.items():
			for request in self.daySchedules[day].deliveries:
				depot[request.toolID] -= request.amount
			print(depot[1]) # of de voorraad van alle tools altijd >= 0 is
			for request in self.daySchedules[day].pickups:
				depot[request.toolID] -= request.amount
			print(depot[1]) # of de voorraad van alle tools altijd >= 0 is

	def amount(self):
		sum = 0
		for request in self.daySchedules:
			#print(request)
			sum += self.daySchedules[request].amount()
		return sum

	def inv(self):
		depot = {}
		minimum=100
		requests = self.instance.requests
		depot = {}
		for toolID, tool in self.instance.tools.items():
			depot[toolID] = tool.available
		for day, daySchedule in self.daySchedules.items():
			for request in self.daySchedules[day].deliveries:
				depot[request.toolID] -= request.amount
				for toolID, tool in self.instance.tools.items():
					if depot[toolID] < minimum:
						minimum = depot[toolID]
			for request in self.daySchedules[day].pickups:
				depot[request.toolID] -= request.amount
		return minimum