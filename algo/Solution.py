from pprint import pprint
from Routing import Routing
from RoutingDay import RoutingDay
from Schedule import Schedule
from ScheduleDay import ScheduleDay
from Trip import Trip
from copy import copy

class Solution:
	def __init__(self, instance, routing=None, txtFile=None):
		self.instance = instance
		if routing:
			self.parseFromRouting(routing)
			self.writeToTxt()
		if txtFile:
			self.parseFromTxt(txtFile)
			self.writeRouting()
			self.calculateInfo()

	def parseFromTxt(self, txtFile):
		array_vars = ['dataset', 'name']
		day = 0
		self.days = {}
		for line in open(txtFile,'r'):
			if line[0].isalpha():
				linelist = line.split('=')
				var = linelist[0].rstrip().lower()
				val = linelist[1].lstrip().rstrip()
				if var in array_vars:
					if val[0].isalpha():
						exec('self.' + var + ' = "' + val + '"')
					else:
						exec('self.' + var + ' = int(' + str(val) + ')')
				elif var == 'day':
					day = int(val)
					self.days[day] = []
			elif line[0].isdigit():
				linelist = line.split('\t')
				index = int(linelist.pop(0))
				option = linelist.pop(0)
				linelist = [int(l) for l in linelist]
				if option is 'R':
					self.days[day].append(linelist)

	def calculateInfo(self):
		self.max_number_of_vehicles = self.routing.maxNumberOfVehicles()
		self.number_of_vehicle_days = self.routing.numberOfVehicleDays()
		self.distance = self.routing.distance()
		self.cost = self.routing.cost()
		self.tool_count = self.routing.toolCount()

	def writeRouting(self):
		self.routing = Routing(self.instance)
		for day, trips in self.days.items():
			routingDay = RoutingDay(self.instance)
			for trip in trips:
				routingDay.addTrip(self.parseTrip(trip))
			self.routing.addRoutingDay(day, routingDay)

	def parseTrip(self, line):
		line = copy(line)
		trip = Trip(self.instance)
		if line[0] == 0:
			del line[0]
		if line[-1] == 0:
			del line[-1]
		for el in line:
			if el < 0:
				request = copy(self.instance.requests[-el])
				request.id *= -1
				request.amount *= -1
			elif el > 0:
				request = copy(self.instance.requests[el])
			else:
				request = 0
			trip.addRequest(request)
		return trip

	def writeSchedule(self):
		self.schedule = Schedule(self.instance)
		for day, trips in self.days.items():
			for trip in trips:
				for id in trip:
					if id < 0:
						self.schedule.addPickupOnDay(day, self.instance.requests[-id])
					elif id > 0:
						self.schedule.addDeliveryOnDay(day, self.instance.requests[id], planPickup=False)

	def parseFromRouting(self, routing):	
		self.dataset = self.instance.dataset
		self.name = self.instance.name
		self.max_number_of_vehicles = routing.maxNumberOfVehicles()
		self.number_of_vehicle_days = routing.numberOfVehicleDays()
		self.tool_use = 0
		self.distance = routing.distance()
		self.cost = routing.cost()
		self.days = {}
		self.routing = routing
		for day, routingDay in routing.routingDays.items():
			tripOutputs = []
			tripOutput = []
			for trip in routingDay.trips:
				if len(trip.requests) > 2:
					for request in trip.requests:
						tripOutput += [0 if isinstance(request, int) else request.id]
				tripOutputs.append(tripOutput)
			self.days[day] = tripOutputs

	def writeToTxt(self, solution_name = "testsolution.txt"):
		file = open(solution_name, 'w')
		file.write("DATASET = " + self.dataset + "\n")
		file.write("NAME = " + self.name + "\n\n")
		file.write("MAX_NUMBER_OF_VEHICLES = " + str(self.max_number_of_vehicles) + "\n")
		file.write("NUMBER_OF_VEHICLE_DAYS = " + str(self.number_of_vehicle_days) + "\n")
		file.write("TOOL_USE = " + str(self.tool_count) + "\n")
		file.write("DISTANCE = " + str(self.distance) + "\n")
		file.write("COST = " + str(self.cost) + "\n\n")
		for day, trips in self.days.items():
			file.write("DAY = " + str(day) + "\n")
			vehicleID = 1
			for trip in trips:
				file.write(str(vehicleID) + '\tR\t' + '\t'.join(str(id) for id in trip) + '\n')
				vehicleID += 1
			file.write('\n')
		file.close()