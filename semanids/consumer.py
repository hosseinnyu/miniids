import sensor
import logging
import collections
import time
import analyzer

#logging.getLogger().setLevel(logging.INFO)

HTTPPacket = collections.namedtuple('HTTPPacket', 'hostname, path, method, dport, sport, src, dst, timestamp')

class Consumer:
	def __init__(self):
		pass
	def plug(self):
		pass

class HttpConsumer(Consumer):
	
	def __init__(self):
		self.sensor = sensor.Sensor()
		self.plugged = collections.defaultdict(list)
		self.analyzers = []
		self.analyzer_mapper = {"FREQUENCY": analyzer.FrequencyAnalyzer}
		self.dashboard_mapper = {"HTTP_URL_FREQUENCY": "getmostfrequent"}

	def plugto(self):
		self.sensor.plug('HTTP', self)
	
	def process(self, httppacket):
		return HTTPPacket(httppacket.Host, httppacket.Path, httppacket.Method, httppacket.dport, httppacket.sport, httppacket.src, httppacket.dst, time.time())
	
	def plug(self, analyzer_type, globalid, target_field, buffer_time_limit):
		a = self.analyzer_mapper[analyzer_type]
		inst = a(globalid, target_field, buffer_time_limit)
		inst.installondashboard(getattr(inst, self.dashboard_mapper[inst.getglobalid()]))
		self.analyzers.append(inst)
		
			
	def notify(self, httppacket):
		stp = self.process(httppacket)

		for s in self.subscribers:
			s.notify(stp)
		
		for a in self.analyzers:
			a.appendentry(stp)

	def start(self):
		self.sensor.start()

if __name__=="__main__":
	hc = HttpConsumer()
	hc.subscribe()
	hc.add_analyzer("FREQUENCY", "HTTP_URL_FREQUENCY", "hostname", 10)
	hc.start()
		
