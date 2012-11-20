import sys
import subprocess
from xml.dom import minidom
from ExecutionFrame import ExecutionFrame


class TestFixture:
	def __init__(self, case_file):
		self.case_list = self.__load_testcases(case_file)
		self.testcase_count = len(self.case_list)
		self.testcases_passed = []
	
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
		return self.__run_tests(executable_path, self.case_list)
		
	def __run_tests(self, testpath, testcases):
		error_msg = ""
		for i in range(0, self.testcase_count):
			test_process = ExecutionFrame(path=testpath,timeout=1,stdin=testcases[i]['input'])
			test_process.Run()
			executionState =  test_process.getTerminateFlag()
			stdout_data = test_process.getOutput()
			
			if (stdout_data.strip() == testcases[i]['output'] and not executionState):
				self.testcases_passed.append(i)
			elif executionState:
				error_msg += "Testcase #" + str(i) + " did not return within the allotted time!\n"
			else:
				error_msg +=  "Testcase #" +  str(i) + " failed!" + "\n"
		return (self.testcase_count - len(self.testcases_passed)), error_msg
			
