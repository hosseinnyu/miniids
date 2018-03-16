import httpconsumer
import threading
import dashboard
import logging
import sys
import sched, time

#logging.getLogger().setLevel(logging.INFO)

class Monitor:
	
	def __init__(self):
		self.consumers = []
		
		hc = httpconsumer.HttpConsumer()
        	self.consumers.append(hc)
		hc.subscribe()
        	hc.add_analyzer("FREQUENCY", "HTTP_URL_FREQUENCY", "hostname", 10)
		self.s = sched.scheduler(time.time, time.sleep)
	
	@staticmethod
	def printstats():
		t = dashboard.Dashboard.getcallee("HTTP_URL_FREQUENCY")()
		#t = "test"
		if t == None:
			t = "Nothing"
		print t
		threading.Timer(5.0, Monitor.printstats).start()

	def start(self):
		threading.Timer(5.0, Monitor.printstats).start()
		for c in self.consumers:
			c.start()

  		#threading.Timer(5.0, Monitor.printstats).start()

if __name__=="__main__":
	m = Monitor()
	m.start()
