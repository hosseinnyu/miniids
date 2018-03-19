import sensor
import logging
import collections
import time
import analyzer
import bisect
from   operator import itemgetter


HTTPPacket = collections.namedtuple('HTTPPacket', 'hostname, path, method, dport, sport, src, dst, timestamp')

class Consumer(object):
	def __init__(self, buffertimelimit):
		self.sensor        = None
                self.buffer        = []
                self.buffer_time_limit   = buffertimelimit
                self.timestamps    = []

	def getdata():
		pass

class HttpConsumer(Consumer):
	
	def __init__(self, buffertimelimit=10):
		super(HttpConsumer, self).__init__(buffertimelimit)

	def plugto(self, sensor):
                self.sensor = sensor
		self.sensor.plugin('HTTP', self)

	def getdata(self, fieldname):
		self.truncateexpired()
		tempbuffer = []
		for f in self.buffer:
			fields = fieldname if isinstance(fieldname, list) else [fieldname]
			v = ",".join([getattr(f, _) for _ in fields])
			tempbuffer.append((getattr(f, "timestamp"),v))
		return (self.timestamps, tempbuffer)

	def process(self, httppacket):
		return HTTPPacket(httppacket.Host, httppacket.Path, httppacket.Method, httppacket.dport, httppacket.sport, httppacket.src, httppacket.dst, time.time())
	
	# removes the old entries from the buffer
        def truncateexpired(self):
                t = time.time()
                loc = bisect.bisect_left(self.timestamps, t-self.buffer_time_limit)
                logging.info("Removing from buffer " + str(loc))
                self.buffer = self.buffer[loc:]
                self.timestamps = self.timestamps[loc:]

	def addtobuffer(self, packet):
                logging.info("Adding to buffer")
                p = self.process(packet)
		self.buffer.append(p)
                self.timestamps.append(getattr(p, "timestamp"))
		self.truncateexpired()
	
	
	def notify(self, httppacket):
		self.addtobuffer(httppacket)
		pass

	def start(self):
		self.sensor.start()

if __name__=="__main__":
	s = sensor.Sensor()
	hc = HttpConsumer()
	hc.plugto(s)
	#hc.subscribe()
	#hc.add_analyzer("FREQUENCY", "HTTP_URL_FREQUENCY", "hostname", 10)
	hc.start()
