"""
	The goal of the dashboard class is to provide a unified access points to stats produced by different cosumers
"""
import collections

class Dashboard:
	dashboard = {}

	def __init__(self):
		pass
	
	@staticmethod
	def install(globalid, callee):
		Dashboard.dashboard[globalid] = callee
	
	@staticmethod
	def getcallee(globalid):
		if globalid in Dashboard.dashboard:
			return Dashboard.dashboard[globalid]
		return None

