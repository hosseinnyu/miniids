import collections
import time
import bisect

class Analyzer:
	def __init__(self, globalid, field_name):
		self.global_id =  globalid
		self.buffer    = []
		self.buffer_time = 10*1000 ## in ms 
		self.field_name = field_name
		self.timestamps = []

	def appendentry(self, data):
		self.buffer.append((getattr(data, "timestamp"),getattr(data, self.field_name)))
		self.timestamps.append(getattr(data, "timestamp"))
		self.truncateexpired()

	def __str__(self):
		return ",".join(map(str, self.buffer))

	# removes the old entries from the buffer
	def truncateexpired(self):
		t = time.time()
		loc = bisect.bisect_left(self.timestamps, t-self.buffer_time)
		self.buffer = self.buffer[loc:]
		self.timestamp = self.buffer[loc:]

class FrequencyAnalyzer(Analyzer):
	def __init__(self, globalid, fieldname):
		Analyzer.__init__(self, globalid, fieldname)
	
	def getcount(self):
		return len(self.buffer)
	

if __name__ == "__main__":
	T = collections.namedtuple('T', 'timestamp, p')
	f = FrequencyAnalyzer("HTTP_URL_FREQ", "p")
	f.appendentry(T(1, "b"))
	f.appendentry(T(2, "c"))
	f.appendentry(T(3, "c"))
	f.truncateexpired()
	#f.appendentry(a"d")
	print f.getcount()
	print f
	
	
