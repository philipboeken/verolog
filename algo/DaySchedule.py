#! /usr/bin/env python

class DaySchedule:

	def __init__(self, self.instance):
		self.pickups = []
		self.deliveries = []

	def addPickup(self, request):
		request.id *= -1
		request.amount *= -1
		self.pickups.append(request)

	def addDelivery(self, request):
		self.deliveries.append(request)

	def deleteDelivery(self, request):
		if request.id in [delivery.id for delivery in self.deliveries]:
			index = 0
			for delivery in self.deliveries:
				if request.equals(delivery):
					index = self.deliveries.index(delivery)
			del self.deliveries[index]
			return True
		else:
			return False

	def deletePickup(self, request):
		request.id *= -1
		if request.id in [pickup.id for pickup in self.pickups]:
			index = 0
			for pickup in self.pickups:
				if request.id == pickup.id:
					index = self.pickups.index(pickup)
			del self.pickups[index]
			return True
		else:
			return False

	def amount(self):
		return len(self.deliveries)
