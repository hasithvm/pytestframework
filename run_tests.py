import sys
import subprocess
from TestFixture import TestFixture
###parses arguments

class CompileException(Exception):
	def __init__(self, message):
		self.message = message.strip()
	def __str__(self):
		return str(self.message)

def compile_source(source_path):
	lang_file  = source_path
	compiler_string = ""	
	ext = lang_file.split(".")[-1].lower()
	if ext == "c":
		compiler_string = "gcc -lm " + lang_file + " -o " + lang_file + ".bin"
		p = subprocess.Popen(compiler_string, stdout=subprocess.PIPE,shell=True)
		resultmsg = p.communicate()[0]
		if (p.returncode != 0):
			raise CompileException(resultmsg)
			
		test_path = lang_file + ".bin"
	if ext == "py":
		test_path = "python " + lang_file
	if ext == "cpp":
		compiler_string = "g++ -lm " + lang_file + "-o " + lang_file + ".bin"
		p = subprocess.Popen(compiler_string, stdout=subprocess.PIPE,shell=True)
		resultmsg = p.communicate()[0]
		if (p.returncode != 0):
			raise CompileException(resultmsg)
		test_path = lang_file + ".bin"

	return test_path




if __name__ == "__main__":
	try:
		test_path = compile_source(sys.argv[1])
	except CompileException as e:
		print e
		sys.exit(2)

	testcases = sys.argv[2]
	tf = TestFixture(testcases)

	if test_path == "":
		print "Invalid file specified!"

	unpassed, err = tf.evaluateTestCases(test_path)
	if unpassed == 0:
		print str(tf.getCasesPassed()) + "/" + str(tf.getCaseCount()), "testcases passed!"
		sys.exit(0)
	else:
		print  str(tf.getCasesPassed()) + "/" + str(tf.getCaseCount()), "testcases passed!"
		print err
		sys.exit(1)
