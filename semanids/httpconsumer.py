import sniffer
import logging
import collections
import time
import analyzer

logging.getLogger().setLevel(logging.INFO)

HTTPPacket = collections.namedtuple('HTTPPacket', 'hostname, path, method, dport, sport, src, dst, timestamp')

class HttpConsumer:
	
	def __init__(self):
		self.sniffer = sniffer.sniffer()
		self.subscribers = collections.defaultdict(list)
		self.analyzers = []
		self.analyzer_mapper = {"FREQUENCY": analyzer.FrequencyAnalyzer}

	def subscribe(self):
		self.sniffer.subscribe('HTTP', self)
	
	def structure(self, httppacket):
		return HTTPPacket(httppacket.Host, httppacket.Path, httppacket.Method, httppacket.dport, httppacket.sport, httppacket.src, httppacket.dst, time.time())
	
	def add_analyzer(self, analyzer_type, globalid, target_field, buffer_time_limit):
		a = self.analyzer_mapper[analyzer_type]
		self.analyzers.append(a(globalid, target_field, buffer_time_limit))
			
	def notify(self, httppacket):
		stp = self.structure(httppacket)

		for s in self.subscribers:
			s.notify(stp)
		
		for a in self.analyzers:
			a.appendentry(stp)
			print a.getmostfrequent()		

		#logging.info(stp)

	def start(self):
		self.sniffer.start()

if __name__=="__main__":
	hc = HttpConsumer()
	hc.subscribe()
	hc.add_analyzer("FREQUENCY", "HTTP_URL_FREQUENCY", "hostname", 10)
	hc.start()
		
