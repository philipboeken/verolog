#! /usr/bin/env python
from copy import copy

class Trip:
	def __init__(self, instance, request=None):
		self.instance = instance
		self.requests = [0,0]
		if request:
			self.addRequest(request)

	def addRequest(self, request, toFront=False):
		if len(self.requests) > 2:
			if toFront:
				del self.requests[0]
				first = 0 if isinstance(self.requests[0], int) else self.requests[0].locationID
				self.requests = [0, copy(request)] + self.requests
			else:
				del self.requests[-1]
				last = 0 if isinstance(self.requests[-1], int) else self.requests[-1].locationID
				self.requests += [copy(request), 0]
		else:
			self.requests = [0, request, 0]


	def deleteRequest(self, request, atEnds=False):
		for req in self.requests:
			if req is not 0:
				if req.equals(request):
					r = req
		if r:
			index = self.requests.index(r)
			prev = 0 if isinstance(self.requests[index-1], int) else self.requests[index-1].locationID
			next = 0 if isinstance(self.requests[index+1], int) else self.requests[index+1].locationID
			del self.requests[index]

	def contains(self, request, atEnds=False):
		if atEnds:
			if request.equals(self.requests[1]) or request.equals(self.requests[-2]):
				return True
		else:
			for r in self.requests:
				if request.equals(r):
					return True
		return False

	def addTrip(self, trip, reverse=False):
		requestList = list(reversed(trip.requests)) if reverse else trip.requests
		for request in requestList:
			if not isinstance(request, int):
				self.addRequest(request)

	def addRoute(self, trip):
		requestList = list(trip.requests)
		for request in requestList:
			if not isinstance(request, int):
				self.requests += [request]
		self.requests += [0]

	def concatenateTrips(self, trip1, trip2, pair):
		if len(trip1.requests) is 3:
			self.addTrip(trip1)
			if len(trip2.requests) is 3:
				self.addTrip(trip2)
			elif trip2.requests[1].equals(pair[1]):
				self.addTrip(trip2)
			else:
				self.addTrip(trip2, True)
		elif trip1.requests[1].equals(pair[0]):
			self.addTrip(trip1, True)
			if len(trip2.requests) is 3:
				self.addTrip(trip2)
			elif trip2.requests[1].equals(pair[1]):
				self.addTrip(trip2)
			else:
				self.addTrip(trip2, True)
		else:
			self.addTrip(trip1)
			if len(trip2.requests) is 3:
				self.addTrip(trip2)
			elif trip2.requests[1].equals(pair[1]):
				self.addTrip(trip2)
			else:
				self.addTrip(trip2, True)

	def isValid(self):
		if self.distance() > self.instance.max_trip_distance:
			return False
		capacity = range(0, self.instance.capacity + 1)
		tools = {}
		for id, tool in self.instance.tools.items():
			tools[id] = [0]
		for request in self.requests:
			for id, ts in tools.items():
				if not isinstance(request, int):
					if id is request.toolID:
						tools[id] += [tools[id][-1] - request.amount*self.instance.tools[request.toolID].size]
					else:
						tools[id] += [tools[id][-1]]
		i = 0
		for id, ts in tools.copy().items():
			m = min(ts)
			tools[id] = [t-m for t in tools[id]]
			i = id
		sumcap = []
		count = 0
		for j in range(0,len(tools[i])):
			for id, ts in tools.items():
				count += ts[j]
			sumcap += [count]
			count=0	
		if max(sumcap) > self.instance.capacity:
			return False
		return True

	def inventoryChange(self):
		inventory = {}
		tools = {}
		for id, tool in self.instance.tools.items():
			tools[id] = [0]
			inventory[id] = 0
		for request in self.requests:
			if not isinstance(request, int):
				if request.amount > 0:
					inventory[request.toolID] += request.amount
				for id, ts in tools.items():
					if not isinstance(request, int):
						if id is request.toolID:
							tools[id] += [tools[id][-1] - request.amount]
						else:
							tools[id] += [tools[id][-1]]
		for id, ts in tools.copy().items():
			m = min(ts)
			if m < 0:
				inventory[id] = inventory[id] + m
		return inventory

	def distance(self):
		prev = 0
		distance = 0
		for request in self.requests:
			if not isinstance(request, int):
				distance += self.instance.distance(prev, request.locationID)
				prev = request.locationID
			else:
				distance += self.instance.distance(prev, 0)
				prev = 0
		return distance

	def equals(self, trip):
		ans = True
		for request in trip.requests:
			if not isinstance(request, int):
				if not self.contains(request):
					ans = False
		return ans

	def returnDeliveries(self):
		deliveries = []
		for request in self.requests:
			if not isinstance(request, int):
				if request.id > 0:
					deliveries.append(request)
		return deliveries

	def returnPickups(self):
		pickups = []
		for request in self.requests:
			if not isinstance(request, int):
				if request.id < 0:
					pickups.append(copy(request))
		return pickups

	def totalToolsNeeded(self):
		inventory = {}
		tools = {}
		for id, tool in self.instance.tools.items():
			tools[id] = [0]
			inventory[id] = 0
		for request in self.requests:
			if not isinstance(request, int):
				for id, ts in tools.items():
					if id is request.toolID:
						tools[id] += [tools[id][-1] - request.amount]
					else:
						tools[id] += [tools[id][-1]]
			else:
				for id, ts in tools.items():
					tools[id] += [tools[id][-1]]   
		for id, ts in tools.items():
			m = min(ts)
			inventory[id] = abs(m)
		return inventory 

	def swapRequests(self, request1, request2):
		req1 = copy(self.requests[request1])
		req2 = copy(self.requests[request2])
		self.requests[request1] = req2
		self.requests[request2] = req1
