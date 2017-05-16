#! /usr/bin/env python
import math
from Request import Request
from Tool import Tool

class Instance:
	def __init__(self, instance_path):
		self.parseInput(instance_path)
		self.remDistanceTable()
		self.convertRequests()
		self.convertTools()
		self.startDepot = {}
		for id, tool in self.tools.items():
			self.startDepot[id] = tool.available

	def parseInput(self, instance_path):
		array_vars = ['tools', 'coordinates', 'requests']
		lastvar = ''
		for line in open(instance_path,'r'):
			if line[0].isalpha():
				linelist = line.split('=')
				var = linelist[0].rstrip().lower()
				if var in array_vars:
					lastvar = var
					exec('self.' + var + ' = {}')
				else:
					val = linelist[1].lstrip().rstrip()
					if val[0].isalpha():
						exec('self.' + var + ' = "' + val + '"')
					else:
						exec('self.' + var + ' = int(' + str(val) + ')')
			elif line[0].isdigit():
				linelist = line.split('\t')
				index = int(linelist.pop(0))
				exec('self.' + lastvar + '[' + str(index) + '] = list(map(int, ' + str(linelist) + '))')

	def distance(self, locID1, locID2):
		x1, y1 = self.coordinates[locID1]
		x2, y2 = self.coordinates[locID2]
		return math.floor(math.sqrt(pow(x1-x2,2) + pow(y1-y2,2)))

	def remDistanceTable(self):
		if 'distance' in self.__dict__.keys():
			del self.distance

	def convertRequests(self):
		for id,request in self.requests.items():
			self.requests[id] = Request(id, request[0], request[1], request[2], request[3], request[4], request[5])

	def convertTools(self):
		for id,tool in self.tools.items():
			self.tools[id] = Tool(id, tool[0], tool[1], tool[2])
