#! /usr/bin/env python
from copy import copy
from ScheduleDay import ScheduleDay

class Schedule:

	def __init__(self, instance):
		self.instance = instance
		self.days = instance.days
		self.scheduleDays = {}
		for day in range(1, self.days + 1):
			self.scheduleDays[day] = ScheduleDay(instance)

	def addDeliveryOnDay(self, day, request):
		self.scheduleDays[day].addDelivery(request)
		self.scheduleDays[day + request.daysStay].addPickup(copy(request))

	def deleteDelivery(self, request):
		for day, scheduleDay in self.scheduleDays.items():
			if scheduleDay.deleteDelivery(request):
				self.scheduleDays[day + request.daysStay].deletePickup(copy(request))
				return True
		return False

	def inventory(self):
		depot = self.instance.startDepot
		minimum=100
		requests = self.instance.requests
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

	def makeInventory(self):
		depot = self.instance.startDepot
		requests = self.instance.requests
		for day, scheduleDay in self.scheduleDays.items():
			for request in self.scheduleDays[day].deliveries:
				depot[request.toolID] -= request.amount
			for toolID, tool in self.instance.tools.items():
				scheduleDay.inventory[toolID] = depot[toolID]
			for request in self.scheduleDays[day].pickups:
				depot[request.toolID] -= request.amount	