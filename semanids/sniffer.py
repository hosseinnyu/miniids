"""
	This module sniffs the network traffic and notifies the subscribers.
"""
from scapy.all import *    #import scapy module to python
from collections import defaultdict
from scapy.layers import http
from scapy.utils import *
import logging

# Singleton class for sniffing the packers and dispatching
class sniffer:
	class __sniffer:
		
		# Different classes can subscribe to this for their intended traffic
		def subscribe(self, traffic_type, handler):
			self.subscribers[traffic_type].append(handler)
			self.traffic_types.add(traffic_type)
		
		# The subscribers get notified as a new packet of the type is arrived
		def process_pkt(self, packet):
			## TODO: also consider HTTP response HTTP Response, check https://github.com/invernizzi/scapy-http

			for tt in self.traffic_types:
				if packet.getlayer(self.layer_mapper[tt]):
					for s in self.subscribers[tt]:
						s.notify(packet)
		
		def listen(self):
			sniff(filter="tcp", iface="enp3s0", prn=self.process_pkt)

		# This need to be called to start the sniffing
		def start(self):
			self.listen()

		def __init__(self):
			self.layer_mapper = {"HTTP": http.HTTPRequest}
			self.subscribers = defaultdict(list)
        		self.traffic_types = set()
	
	## enforcing singleton
	instance = None
	
	def __init__(self):
		logging.info("Initializing HTTP sniffer")
		if not sniffer.instance:
			sniffer.instance = sniffer.__sniffer()
	
	def __getattr__(self, name):
		return getattr(self.instance, name)


if __name__ == "__main__":
	s = sniffer()
