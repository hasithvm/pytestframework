import threading, subprocess
class ExecutionFrame(threading.Thread):
	def __init__(self, *args, **kwargs):
		threading.Thread.__init__(self)
		self.path = kwargs.get('path', None)
		self.timeout = int(kwargs.get('timeout', 1))
		self.stdin = kwargs.get('stdin', None)
		self.terminate_flag = False

	def run(self):
		self.process_handle=subprocess.Popen(self.path,stdout=subprocess.PIPE, stdin=subprocess.PIPE,shell=False)
		if (self.stdin != None):
			self.output = self.process_handle.communicate(self.stdin)[0].strip()
		else:
			self.output = self.process_handle.communicate()[0].strip()
		self.returncode = self.process_handle.returncode

	def Run(self):
		self.start()
		self.join(self.timeout)
		
		if self.is_alive():
			#the process has now exceeded its given time, kill it.
			self.process_handle.kill()
			#set the terminate flag to make sure the caller knows we killed it.
			self.terminate_flag = True
			self.join()

		
	def getReturnCode(self):
		return self.returncode
		
	def getOutput(self):
		return self.output		
	def getTerminateFlag(self):
		return self.terminate_flag
