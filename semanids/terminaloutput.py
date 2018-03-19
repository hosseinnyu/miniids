import time
import collections
import os
import threading

SCREEN_REFRESH_INTERVAL = 2

screensection = collections.namedtuple("screensections", "id, title, maxheight")

class TerminalOutput(object):
	
	def __init__(self, sections=[]):
		os.system('clear')
		self.sections = sections
		self.buffer   = collections.defaultdict(list)

	def printheader(self):
		print "Hossein's IDS"

	def addsection(self, section):
		self.sections.append(section)
	
	def addstr(self, sectionid, msgline):
		self.buffer[sectionid].append(msgline)

	def refresh(self):
		#return	
		os.system('clear')
		
		self.printheader()
		cr  = 0
		for s in self.sections:
			sr = 1
			print ("+++++++++++++++++++++++++%s")%(s.title)
			for e in reversed(self.buffer[s.id]):
				if sr>s.maxheight:
					break
				print sr, e
				sr += 1
		
			
		threading.Timer(SCREEN_REFRESH_INTERVAL, self.refresh).start()
	
	def start(self):
		threading.Timer(SCREEN_REFRESH_INTERVAL, self.refresh).start()

if __name__== "__main__":
	os.system('clear')  
	print "hi"
	os.system('clear')
	print "bye"
	t = TerminalOutput()
	t.addsection(screensection("alert", "IDS Alerts", 10))
	t.addstr("alert", "emergency")
	t.start()
