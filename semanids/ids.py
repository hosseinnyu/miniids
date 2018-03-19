import time
import dashboard
import sys
import collections

idsmessage = collections.namedtuple("idsmessage", "messagetype, message, timestamp")

class IDS(object):
	
	def __init__(self):
		self.meters = []
		self.monitor = None

	def plugto(self, meterglobalid):
		self.meters.append(meterglobalid)
	
	def plug(self, monitor):
		self.monitor = monitor
	
	def notify(self, msg):
		if self.monitor!=None:
			self.monitor.notify(msg)
	
	def check(self):
		meter_values = {}
		for s in self.meters:
			meter_values[s] = dashboard.Dashboard.getcallee(s).getanalysis()
		
		## one example rule
		if ("HTTP_URL_FREQUENCY_2M" in meter_values) and (meter_values["HTTP_URL_FREQUENCY_2M"][0]>3):
			msg = idsmessage("ALERT", ("High traffic generated an alert - hits %s, triggered at %s")%(meter_values["HTTP_URL_FREQUENCY_2M"][0], time.time()), time.time())
			self.notify(msg)

		if ("HTTP_URL_FREQUENCY_10S" in meter_values):
			msg = idsmessage("NOTIFICATION",  str(meter_values["HTTP_URL_FREQUENCY_10S"]), time.time())
			self.notify(msg)
			
