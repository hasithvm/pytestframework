import threading, subprocess
class BaseExecutionFrame(threading.Thread):
	def __init__(self, *args, **kwargs):
		threading.Thread.__init__(self)
		self.path = kwargs.get('path', None)
		self.timeout = int(kwargs.get('timeout', 1.0))
		self.stdin = kwargs.get('stdin', None)
		self.terminate_flag = False
		self.output = None
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
	
	
	def Run(self):
		pass
	
		
		
	def getReturnCode(self):
		return self.returncode
		
	def getOutput(self):
		return self.output		
	def getTerminateFlag(self):
		return self.terminate_flag
	def getCustomProcessIdentifer(self):
		return self.custompid

class SynchExecutionFrame(BaseExecutionFrame):
	def __init__(self,*args, **kwargs):
		BaseExecutionFrame.__init__(self,*args,**kwargs)
	
	def Run(self):
		self.start()
		self.join(self.timeout)
		if self.is_alive():
			#the process has now exceeded its given time, kill it.
			self.process_handle.kill()
			#set the terminate flag to make sure the caller knows we killed it.
			self.terminate_flag = True
			self.join()

class AsyncExecutionFrame(BaseExecutionFrame):
	def __init__(self, *args,**kwargs):
		BaseExecutionFrame.__init__(self, *args, **kwargs)
		self.callback = kwargs.get('callback', None)

	def Run(self):
		if (self.completion_handler == None):
			raise Exception("No callback function for asynchronous execution.")
		self.completion_timer = threading.Timer(self.timeout, self.timeout_handler)
		self.completion_timer.start()
		self.start()

	def run(self):
		BaseExecutionFrame.run(self)
		self.completion_handler()

	def timeout_handler(self):
		if self.is_alive():
			print "killing hung process"
			self.process_handle.kill()
			self.terminate_flag = True
			self.completion_handler()

	def completion_handler(self):
		self.callback(self)
