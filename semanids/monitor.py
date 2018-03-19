import consumer
import sensor
import analyzer
import threading
import dashboard
import logging
import sys
import sched, time
import ids
import terminaloutput
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
		self.ids.plug(self)		

		self.terminal = terminaloutput.TerminalOutput()
		self.terminal.addsection(terminaloutput.screensection("ALERT", "IDS Alerts", 10))
		self.terminal.addsection(terminaloutput.screensection("NOTIFICATION", "IDS Notifications", 20))
		self.terminal.start()

		self.consumers.append(hc)
                #self.s = sched.scheduler(time.time, time.sleep)

	
	def notify(self, msg):
		#print msg.messagetype, msg.message
		self.terminal.addstr( msg.messagetype, msg.message + " " + str(msg.timestamp))

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
