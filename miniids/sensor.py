## @package sensor
#  This module senses the network traffic and notifies the plugged objects.

from scapy.all import *    #import scapy module to python
from collections import defaultdict
from scapy.layers import http
from scapy.utils import *
import logging
import ConfigParser as configparser
import os.path

## Documentation for Sensor
#  This is a singleton class for sniffing the packers and dispatching the events when a new packet arrives
class Sensor:
	
	## Documentation for __sensor
	#  This is a private class that can only be accessed from within Sensor. The goal is to make Sensor a singleton class
	class __sensor:
		
		# Upper layers can plug to sensor and consume data
		def plugin(self, traffic_type, handler=None):

			if handler is None:
				raise ValueError("The handler can't be None.")
			
			notify_func = getattr(handler, "notify", None)
			if not callable(notify_func):
    				raise ValueError("The handler object must have a notify method.")

			if not traffic_type in self.layer_mapper:
				raise ValueError(("The traffic type %s is not currently supported.")%(traffic_type))
			
			self.plugged[traffic_type].append(handler)
			self.traffic_types.add(traffic_type)
		
		# The subscribers get notified as a new packet of the type is arrived
		def notify(self, packet):
			## TODO: also consider HTTP response HTTP Response, check https://github.com/invernizzi/scapy-http

			for tt in self.traffic_types:
				if packet.getlayer(self.layer_mapper[tt]):
					for s in self.plugged[tt]:
						s.notify(packet)
		
		## Initializes a sniffer to listen to a specified network interface
		def listen(self):
			if not self.interface:
				raise ValueError("The interface can't be None.")
			try:
				sniff(filter="tcp", iface= self.interface, prn=self.notify)
			except socket.error:
				raise ValueError(("The interface %s does not exist")%(self.interface))

		## Call start so start listening to the network traffic 
		def start(self):
			self.listen()
		
		## The class initializer
		def __init__(self, interface=None):
			self.interface     = None

			if interface == None:

				## Reading the configurations from the config file
				script_dir       = os.path.dirname(__file__)
				config_file_addr =  os.path.join(script_dir, "../config.txt")
				if not os.path.isfile(config_file_addr):
					raise ValueError(("The config file does not exists in %s .")%(config_file_addr))
				
				config             = configparser.ConfigParser()
				config.read(config_file_addr)
				self.interface     = config.get("sensorconfig", "Interface")
			
			else:
				self.interface = interface
			
			self.layer_mapper  = {"HTTP": http.HTTPRequest}
                        self.plugged       = defaultdict(list)
                        self.traffic_types = set()

	## a variable that enforces singleton. If @var instance is null, no instance of the class is initialzed.
	instance = None
	
	## A method initializing the singleton class
	def __init__(self):
		logging.info("Initializing HTTP Sensor")
		if not Sensor.instance:
			Sensor.instance = Sensor.__sensor()
	
	## A method that bypass the function calls to the private inner class
	def __getattr__(self, name):
		return getattr(self.instance, name)

## run this for an independent execution of this class 
if __name__ == "__main__":
	s = Sensor()
	s.start()
