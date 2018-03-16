import collections
import time
import bisect
from operator import itemgetter
import logging
import dashboard

class Analyzer:

	def __init__(self, globalid, field_name, buffer_time_limit):
		self.global_id =  globalid
		self.buffer    = []
		self.buffer_time = buffer_time_limit#10*1000 ## in ms 
		self.field_name = field_name
		self.timestamps = []

	# adds an entry to the buffer
	def appendentry(self, data):
		logging.info("Adding to buffer")
		self.buffer.append((getattr(data, "timestamp"),getattr(data, self.field_name)))
		self.timestamps.append(getattr(data, "timestamp"))
		self.truncateexpired()

	# removes the old entries from the buffer
	def truncateexpired(self):
		t = time.time()
		loc = bisect.bisect_left(self.timestamps, t-self.buffer_time)
		logging.info("Removing from buffer " + str(loc))
		self.buffer = self.buffer[loc:]
		self.timestamps = self.timestamps[loc:]

	def installondashboard(self, f):
		dashboard.Dashboard.install(self.global_id, f)

	def getglobalid(self):
		return self.global_id

	def __str__(self):
                return ",".join(map(str, self.buffer))


class FrequencyAnalyzer(Analyzer):
	def __init__(self, globalid, fieldname, buffer_time_limit):
		Analyzer.__init__(self, globalid, fieldname, buffer_time_limit)
	
	# gives the number of elements in the buffer
	def getcount(self):
		return len(self.buffer)
	
	# gives the most frequent item and number of occurances
	def getmostfrequent(self):
		if len(self.buffer)==0:
			return None

		s = [_[1] for _ in self.buffer]
		s = collections.Counter(s)
		
		m_value = 0
		m_count = 0
		for _ in s:
			if s[_]>m_count:
				m_count = s[_]
				m_value = _
		return (m_value, m_count)			
		
	

if __name__ == "__main__":
	T = collections.namedtuple('T', 'timestamp, p')
	f = FrequencyAnalyzer("HTTP_URL_FREQ", "p", 10*1000)
	f.appendentry(T(1, "b"))
	f.appendentry(T(2, "c"))
	f.appendentry(T(3, "c"))
	f.appendentry(T(4, "b"))
	f.appendentry(T(4, "b"))
	f.appendentry(T(4, "b"))
	#f.truncateexpired()
	#f.appendentry(a"d")
	print f.getcount()
	print f.getmostfrequent()
