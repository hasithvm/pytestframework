import sys
import subprocess
from xml.dom import minidom
from ExecutionFrame import AsyncExecutionFrame
import threading

class TestFixture:
	def __init__(self, case_file):
		self.case_list = self.__load_testcases(case_file)
		self.testcase_count = len(self.case_list)
		self.testcases_passed = []
		self.error_msg = ""
		self.test_complete = threading.Event()
	
	def getCaseCount(self):
		return self.testcase_count
	
	def getCasesPassed(self):
		return len(self.testcases_passed)
		
	def __load_testcases(self, case_file):
		xmltree = minidom.parse(case_file)
		cases = xmltree.getElementsByTagName('case')
		case_list = []
		
		for case in cases:
			case_dict = dict()
			for child in case.childNodes:
				for valnode in child.childNodes:
					if valnode:
						case_dict[valnode.parentNode.attributes['datatype'].value] = valnode.nodeValue.decode('utf-8').strip()
			case_list.append(case_dict)	
		return case_list

	def evaluateTestCases(self, executable_path):
		if executable_path == "":
			raise Exception("Can't find executable to test!")
		self.test_complete.clear()
		self.__run_tests(executable_path)
		self.test_complete.wait()
		return (self.testcase_count - len(self.testcases_passed)), self.error_msg
	def __run_tests(self, testpath):
		error_msg = ""
		self.testcases_left = self.testcase_count	
		for i in range(0, self.testcase_count):
			test_process = AsyncExecutionFrame(path=testpath,timeout=1.0,stdin=self.case_list[i]['input'],callback = self.__run_test_callback, identifier=i)
			
			test_process.Run()
			
	def __run_test_callback(self, test_process):
		testid = test_process.getCustomProcessIdentifer()
		executionState =  test_process.getTerminateFlag()
		stdout_data = test_process.getOutput()
		self.testcases_left= self.testcases_left -1
		if (stdout_data == self.case_list[testid]['output'] and not executionState):
			self.testcases_passed.append(testid)
		elif executionState:
			self.error_msg += "Testcase #" + str(testid) + " did not return within the allotted time!\n"
		else:
			self.error_msg +=  "Testcase #" +  str(testid) + " failed!" + "\n"
		if (self.testcases_left == 0):
			print "all testcases complete"
			self.test_complete.set()		
