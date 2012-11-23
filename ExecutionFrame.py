import threading, subprocess
class ExecutionFrame(threading.Thread):
	def __init__(self, *args, **kwargs):
		threading.Thread.__init__(self)
		self.path = kwargs.get('path', None)
		self.timeout = int(kwargs.get('timeout', 1))
		self.stdin = kwargs.get('stdin', None)
		self.terminate_flag = False
		self.output = None
		self.callback = kwargs.get('callback', None)
		self.custompid = kwargs.get('identifier', 0)

	def run(self):
		if (self.path == None):
			raise Exception("Could not find executable path!")
		self.process_handle=subprocess.Popen(self.path,stdout=subprocess.PIPE, stdin=subprocess.PIPE,shell=True)
		if (self.stdin != None):
			self.output = self.process_handle.communicate(self.stdin)[0].strip()
		else:
			self.output = self.process_handle.communicate()[0].strip()
		self.returncode = self.process_handle.returncode
	
	def completion_handler(self):
		if self.is_alive():
			print "killing hung process"
			self.process_handle.kill()
			self.terminate_flag = True
			self.join()
		if (self.callback != None):
			self.callback(self)
	def Run(self):
		self.completion_timer = threading.Timer(1.0, self.completion_handler)
		self.completion_timer.start()
		self.start()

		""""self.join(self.timeout)
		
		if self.is_alive():
			#the process has now exceeded its given time, kill it.
			self.process_handle.kill()
			#set the terminate flag to make sure the caller knows we killed it.
			self.terminate_flag = True
			self.join()
		"""
		
	def getReturnCode(self):
		return self.returncode
		
	def getOutput(self):
		return self.output		
	def getTerminateFlag(self):
		return self.terminate_flag
	def getCustomProcessIdentifer(self):
		return self.custompid
