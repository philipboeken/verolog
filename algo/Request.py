#! /usr/bin/env python

class Request:
	
	def __init__(self, id, locationID, firstDay, lastDay, daysStay, toolID, amount):
		self.id = id
		self.locationID = locationID
		self.firstDay = firstDay
		self.lastDay = lastDay
		self.daysStay = daysStay
		self.toolID = toolID
		self.amount = amount
		
	def toString(self):
		s = ''
		for key, val in self.__dict__.items():
			s += str(key) + ': ' + str(val) + ' '
		return s

	def equals(self, request):
		if isinstance(request, int):
			return False
		else:
			return self.id is request.id
