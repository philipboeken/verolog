from pprint import pprint

class Solution:

	def __init__(self, instance, routing):
		self.parseRouting(instance, routing)

	def parseRouting(self, instance, routing):	
		self.dataset = instance.dataset
		self.name = instance.name
		self.max_number_of_vehicles = routing.maxNumberOfVehicles()
		self.number_of_vehicle_days = routing.numberOfVehicleDays()
		self.tool_use = 0
		self.distance = routing.distance()
		self.cost = instance.vehicle_cost*self.max_number_of_vehicles+instance.vehicle_day_cost*self.number_of_vehicle_days+instance.distance_cost*self.distance
		self.days = []
		self.routing = routing
		for day, routingDay in routing.routingDays.items():
			tripOutputs = []
			tripOutput = []
			vehicleID = 0
			for trip in routingDay.trips:
				if len(trip.requests) > 2:
					vehicleID += 1
					tripOutput = [vehicleID, 'R']
					for request in trip.requests:
						tripOutput += [0 if isinstance(request, int) else request.id]
				tripOutputs.append(tripOutput)
			self.days.append({'day':day, 'number_of_vehicles': routingDay.numberOfVehicles, 'trips': tripOutputs})

	def writeSolution(self, solution_name = "sol1.txt"):
		file = open(solution_name, 'w')
		file.write("DATASET = " + self.dataset + "\n")
		file.write("NAME = " + self.name + "\n\n")
		file.write("MAX_NUMBER_OF_VEHICLES = " + str(self.max_number_of_vehicles) + "\n")
		file.write("NUMBER_OF_VEHICLE_DAYS = " + str(self.number_of_vehicle_days) + "\n")
		#file.write("TOOL_USE = " + str(self.tool_use) + "\n")
		file.write("DISTANCE = " + str(self.distance) + "\n")
		file.write("COST = " + str(self.cost) + "\n\n")
		for day in self.days:
			if day['trips']:
				file.write("DAY = " + str(day['day']) + "\n")
				file.write("NUMBER_OF_VEHICLES = " + str(day['number_of_vehicles']) + "\n")
				for trip in day['trips']:
					file.write(' '.join(str(id) for id in trip) + '\n')
				file.write('\n')
		file.close()