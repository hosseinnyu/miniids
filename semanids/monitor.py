import consumer
import sensor
import analyzer
import threading
import dashboard
import logging
import sys
import sched, time
import ids
#logging.getLogger().setLevel(logging.INFO)

IDS_CHECK_INTERVAL = 5

class Monitor:
	
	def __init__(self):
		self.consumers = []
		s  = sensor.Sensor()
        	hc = consumer.HttpConsumer()
        	hc.plugto(s)

        	fa = analyzer.FrequencyAnalyzer( "HTTP_URL_FREQUENCY_10S", "hostname", 10)
        	fa.plugto(hc)

		fa2 = analyzer.FrequencyAnalyzer( "HTTP_URL_FREQUENCY_2M", "hostname", 10)
                fa2.plugto(hc)

		self.ids = ids.IDS()
		self.ids.plugto("HTTP_URL_FREQUENCY_10S")
		self.ids.plugto("HTTP_URL_FREQUENCY_2M")

		self.consumers.append(hc)
		self.s = sched.scheduler(time.time, time.sleep)
	
	def visitids(self):
		self.ids.check()
		threading.Timer(IDS_CHECK_INTERVAL, self.visitids).start()

	def start(self):
		threading.Timer(IDS_CHECK_INTERVAL, self.visitids).start()
		for c in self.consumers:
			c.start()

if __name__=="__main__":
	m = Monitor()
	m.start()
