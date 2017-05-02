#! /usr/bin/env python

import argparse
from Instance import Instance
from Solution import Solution

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Read and checks CVRPTWUI solution file.')
	parser.add_argument('--solution', '-s', metavar='SOLUTION_FILE', required=True, help='The solution file')
	parser.add_argument('--instance', '-i', metavar='INSTANCE_FILE', required=True, help='The instance file')
	args = parser.parse_args()

	instance = Instance(args.instance)

	solution = Solution(instance, args.solution)

	errors = solution.hasErrors()

	ans = 'The solution is invalid' if errors else 'The solution is valid'
	print(ans)
	
	if errors:
		for error in errors:
				print(error)
	else:
		print('Max number of vehicles: ' + str(solution.max_number_of_vehicles))
		print('Number of vehicle days: ' + str(solution.number_of_vehicle_days))
		print('Distance: ' + str(solution.distance))
		print('Cost: ' + str(solution.cost))
		print('Tool count: ' + str(solution.tool_count))
