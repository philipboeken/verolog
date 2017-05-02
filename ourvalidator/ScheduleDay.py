#! /usr/bin/env python

class ScheduleDay:

	def __init__(self):
		self.pickups = []
		self.deliveries = []

	def __str__(self):
		s = 'Deliveries: \n'
		for delivery in self.deliveries:
			s += str(delivery) + '\n'
		s += 'Pickups: \n'
		for pickup in self.pickups:
			s += str(pickup) + '\n'
		return s

	def addPickup(self, request):
		request.id *= -1
		request.amount *= -1
		self.pickups.append(request)

	def addDelivery(self, request):
		self.deliveries.append(request)
		