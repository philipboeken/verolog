from Schedule import Schedule
from pprint import pprint
import random
from copy import copy

class InitSchedule:

	def __init__(self, instance):
		self.instance = instance
		self.schedule = self.createSchedule()

	def createSchedule(self):
		schedule = Schedule(self.instance)
		for id, request in self.instance.requests.items():
			schedule.addDeliveryOnDay(request.firstDay, request)
		minimum = schedule.inv()
		tresh = 0.3
		best = Schedule(self.instance)
		while tresh > 0:
			day = random.randint(1,self.instance.days)
			while len(schedule.daySchedules[day].deliveries) is 0:
				day = random.randint(1,self.instance.days)
			request = schedule.daySchedules[day].deliveries[random.randint(0,len(schedule.daySchedules[day].deliveries)-1)]
			offset = random.randint(request.firstDay,request.lastDay)
			schedule.deleteDelivery(request)
			schedule.addDeliveryOnDay(offset, request) 
			if schedule.inv() < minimum and random.random() > tresh:
				schedule.deleteDelivery(request)
				schedule.addDeliveryOnDay(day, request) 
			if schedule.inv() > minimum and schedule.isValidShort():
				minimum = copy(schedule.inv())
				best = copy(schedule)
			if best.isValidShort() and minimum > 0:
					tresh -= 0.00001
			print(best.isValidShort())
			print(minimum)
		return schedule
