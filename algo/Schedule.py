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
			self.daySchedules[day] = DaySchedule(instance)

	def addDeliveryOnDay(self, day, request):
		self.daySchedules[day].addDelivery(request)
		self.daySchedules[day + request.daysStay].addPickup(copy(request))

	def deleteDelivery(self, request):
		for day, daySchedule in self.daySchedules.items():
			if daySchedule.deleteDelivery(request):
				self.daySchedules[day + request.daysStay].deletePickup(copy(request))
				return True
		return False

	def inventory(self):
		depot = {}
		minimum=100
		requests = self.instance.requests
		for toolID, tool in self.instance.tools.items():
			depot[toolID] = tool.available
		for day, daySchedule in self.daySchedules.items():
			for request in self.daySchedules[day].deliveries:
				depot[request.toolID] -= request.amount
			for request in self.daySchedules[day].pickups:
				depot[request.toolID] -= request.amount	
			for toolID, tool in self.instance.tools.items():
				if depot[toolID] < minimum:
					minimum = depot[toolID]
		return minimum

	def makeInventory(self):
		depot = {}
		requests = self.instance.requests
		for toolID, tool in self.instance.tools.items():
			depot[toolID] = tool.available
		for day, daySchedule in self.daySchedules.items():
			for request in self.daySchedules[day].deliveries:
				depot[request.toolID] -= request.amount
			for toolID, tool in self.instance.tools.items():
				daySchedule.inventory[toolID] = depot[toolID]
			for request in self.daySchedules[day].pickups:
				depot[request.toolID] -= request.amount	