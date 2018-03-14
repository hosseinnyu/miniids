import sniffer
import logging
logging.getLogger().setLevel(logging.INFO)
class HttpConsumer:
	def __init__(self):
		self.sniffer = sniffer.sniffer()
	
	def subscribe(self):
		self.sniffer.subscribe('HTTP', self)
	
	def notify(self, httppacket):
		print httppacket.Host

	def start(self):
		self.sniffer.start()

if __name__=="__main__":
	hc = HttpConsumer()
	hc.subscribe()
	hc.start()
		
