def count_vowels(inputstr):
	text = inputstr.lower()
	vowels = 'aeiou'
	vc = 0
	for char in text:
		if char in vowels:
			vc = vc + 1
	return vc

lines = []


vowelcount = 0

while (True):
	try:
		readln = raw_input()
		lines.append(readln)
		
	except EOFError:
		break	
vc = 0
for i in range(ord('A'), ord('Z') + 1):
	vc = 0
	for line in lines:
		if line[0].upper() == chr(i):
			vc = vc + 1
	if (vc != 0):
		print chr(i) + ":" + str(vc)


