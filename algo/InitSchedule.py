from Schedule import Schedule
from pprint import pprint
import random

class InitSchedule:

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
			day = random.randint(1,len(schedule.daySchedules))
			while len(schedule.daySchedules[day].deliveries)==0:
				day = random.randint(1,len(schedule.daySchedules))
			request = schedule.daySchedules[day].deliveries[random.randint(0,len(schedule.daySchedules[day].deliveries)-1)]
			offset = random.randint(request.firstDay,request.lastDay)
			schedule.deleteDelivery(request)
			schedule.addDeliveryOnDay(offset, request)
			newMinimum = schedule.inventory()
			if newMinimum < minimum:
				schedule.deleteDelivery(request)
				schedule.addDeliveryOnDay(day, request)
			if newMinimum == minimum:
				i = 0
			if newMinimum > minimum:
				i = i+1 
			else:
				minimum = schedule.inventory()
		schedule.makeInventory()
		return schedule
