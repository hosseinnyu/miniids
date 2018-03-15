import sniffer
import logging
import collections
import time

logging.getLogger().setLevel(logging.INFO)

HTTPPacket = collections.namedtuple('HTTPPacket', 'hostname, path, method, dport, sport, src, dst, timestamp')

class HttpConsumer:
	
	def __init__(self):
		self.sniffer = sniffer.sniffer()
		self.subscribers = defaultdict(list)
		self.analyzers = list
	
	def subscribe(self):
		self.sniffer.subscribe('HTTP', self)
	
	def structure(self, httppacket):
		return HTTPPacket(httppacket.Host, httppacket.Path, httppacket.Method, httppacket.dport, httppacket.sport, httppacket.src, httppacket.dst, time.time())

	def notify(self, httppacket):
		stp = self.structure(httppacket)

		for s in self.subscribers:
			s.notify(stp)
		
		for a in self.analyzers:
			a.analyze(stp)		

		logging.info(stp)

	def start(self):
		self.sniffer.start()

if __name__=="__main__":
	hc = HttpConsumer()
	hc.subscribe()
	hc.start()
		
