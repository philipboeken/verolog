#! /usr/bin/env python
import operator

class TwoOpt:
	def __init__(self, instance, routing):
		self.instance = instance
		self.routing = routing
		self.algorithm()

	def algorithm(self):
		for day in self.routing.routingDays:
			for trip in self.routing.routingDays[day].trips:
				ready = False
				while not ready:
					savings = self.createSavingsList(trip)
					if not savings:
						ready = True
					for pair, saving in savings:
						request1 = pair[0]+1
						request2 = pair[1] +1
						trip.swapRequests(request1,request2)
						if not trip.isValid():
							trip.swapRequests(request1,request2)
						else:
							ready = False
							break
						ready = True
			self.routing.routingDays[day].mergeTrips()

	def createSavingsList(self, trip):
		savings = {}
		for request1 in range(1,len(trip.requests)-4):
			for request2 in range(request1+2,len(trip.requests)-2):
				first = self.routing.cost()
				req1 = request1 +1
				req2 = request2 +1
				trip.swapRequests(req1,req2)
				second = self.routing.cost()
				trip.swapRequests(req1,req2)
				if first - second > 0:
					savings[(request1,request2)] = first - second
		return sorted(savings.items(), key=operator.itemgetter(1), reverse=True)
