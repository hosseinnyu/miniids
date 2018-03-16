import time
import dashboard
import sys

class IDS(object):
	
	def __init__(self):
		self.meters = []

	def plugto(self, meterglobalid):
		self.meters.append(meterglobalid)

	def check(self):
		meter_values = {}
		for s in self.meters:
			meter_values[s] = dashboard.Dashboard.getcallee(s).getanalysis()
		
		## one example rule
		if ("HTTP_URL_FREQUENCY_2M" in meter_values) and (meter_values["HTTP_URL_FREQUENCY_2M"][0]>3):
			#s = ("High traffic generated an alert - hits %s, triggered at %s")%(meter_values["HTTP_URL_FREQUENCY_2M"][0], time.time())
			#sys.stdout.write("Alert: : %s%%   \r" % (s) )
			#sys.stdout.flush()
			#print ("High traffic generated an alert - hits %s, triggered at %s")%(meter_values["HTTP_URL_FREQUENCY_2M"][0], time.time())

		if ("HTTP_URL_FREQUENCY_10S" in meter_values):
			print meter_values["HTTP_URL_FREQUENCY_10S"]
			
