#! /usr/bin/env python
from Schedule import Schedule
import random

class ScheduleMaker:
	def __init__(self, instance):
		self.instance = instance
		self.schedule = self.createSchedule()

	def createSchedule(self):
		i = 0
		schedule = Schedule(self.instance)
		for id, request in self.instance.requests.items():
			schedule.addDeliveryOnDay(request.firstDay, request)
		minimum = schedule.inventory()
		while i < 1500:
			day = random.randint(1, len(schedule.scheduleDays))
			while len(schedule.scheduleDays[day].deliveries) is 0:
				day = random.randint(1,len(schedule.scheduleDays))	
			request = schedule.scheduleDays[day].deliveries[random.randint(0, len(schedule.scheduleDays[day].deliveries)-1)]
			offset = random.randint(request.firstDay,request.lastDay)
			schedule.deleteDelivery(request)
			schedule.addDeliveryOnDay(offset, request) 
			newMinimum = schedule.inventory() 
			if newMinimum < minimum:
				schedule.deleteDelivery(request)
				schedule.addDeliveryOnDay(day, request)
			else:
				i = i+1 if newMinimum is minimum else 0
				minimum = newMinimum
		schedule.makeInventory()
		return schedule
