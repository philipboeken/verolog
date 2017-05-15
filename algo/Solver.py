#! /usr/bin/env python
from Instance import Instance
from Strategy1 import Strategy1
import sys

if __name__ == "__main__":
	args = sys.argv
	instance = Instance(args[1])
	strategy = Strategy1(instance)
	strategy.solution.writeSolution(args[2])