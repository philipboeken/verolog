#! /usr/bin/env python

import argparse, copy
from Instance import Instance
from Solution import Solution
from pprint import pprint

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Read and checks CVRPTWUI solution file.')
	parser.add_argument('--solution', '-s', metavar='SOLUTION_FILE', required=True, help='The solution file')
	parser.add_argument('--instance', '-i', metavar='INSTANCE_FILE', required=True, help='The instance file')
	args = parser.parse_args()

	instance = Instance(args.instance)

	solution = Solution(instance, txtFile=args.solution)

	solution.writeSchedule()

	routingErrors = solution.routing.hasErrors()
	scheduleErrors = solution.schedule.hasErrors()
	valid = not routingErrors and not scheduleErrors

	print('Max number of vehicles: ' + str(solution.max_number_of_vehicles))
	print('Number of vehicle days: ' + str(solution.number_of_vehicle_days))
	print('Distance: ' + str(solution.distance))
	print('Cost: ' + str(solution.cost))
	print('Tool count: ' + str(solution.tool_count))

	ans = 'The schedule is valid!' if valid else 'The schedule is invalid!'
	print(ans)

	if not valid:
		for error in scheduleErrors + routingErrors:
				print(error)
