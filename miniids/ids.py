import time
import dashboard
import sys
import collections

idsmessage = collections.namedtuple("idsmessage", "messagetype, message, timestamp")

class IDS(object):
	
	def __init__(self):
		self.meters = []
		self.monitor = None
		self.alertstate = False		

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
		THREASHOLD = 20
		
		if ("HTTP_URL_FREQUENCY_2M" in meter_values):
			if (meter_values["HTTP_URL_FREQUENCY_2M"][0]>=THREASHOLD) and self.alertstate==False:
				msg = idsmessage("ALERT", ("High traffic generated an alert - hits %s ")%(meter_values["HTTP_URL_FREQUENCY_2M"][0]), time.time())
				self.notify(msg)
				self.alertstate = True
			if self.alertstate and (meter_values["HTTP_URL_FREQUENCY_2M"][0]<THREASHOLD):
				msg = idsmessage("ALERT", ("Traffic back to normal - hits %s")%(meter_values["HTTP_URL_FREQUENCY_2M"][0]), time.time())
				self.notify(msg)
				self.alertstate = False

		if ("HTTP_URL_FREQUENCY_10S" in meter_values):
			if meter_values["HTTP_URL_FREQUENCY_10S"][0]!=0:
				msg = idsmessage("NOTIFICATION",  ("Total Req:%s, Most Freq:%s, URL:%s")%(meter_values["HTTP_URL_FREQUENCY_10S"][0], meter_values["HTTP_URL_FREQUENCY_10S"][2], meter_values["HTTP_URL_FREQUENCY_10S"][1]), time.time())
				self.notify(msg)
			
