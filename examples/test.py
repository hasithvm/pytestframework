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

for line in lines:
	vowelcount = vowelcount + count_vowels(line)
	
print vowelcount	

