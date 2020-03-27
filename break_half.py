
#input a subtitle file with long text this script will break
#it into two lines

import sys
import re

with open(sys.argv[1]) as f:
	lines = f.readlines()

def findSpace(letters):

	#print("Iam1",letters)
	if(re.search(r' ',letters, re.UNICODE)):
		#print("Iam2",letters)
		flag = 0
		l = len(letters)
		#print("iam",l)
		for i in range(round(l/2),round(l/2)+10):
		#for i in range(41,46):
			for m in re.finditer(' ',letters):
				#print("Iam ehre",i,m,letters)
				if(m.end() == i):
					flag = 1
					#print("Iam1",flag)
					return letters[0:i-1] + "\n" + letters[i:]
			if(flag == 1):
				break
		for i in range(round(l/2)-10,round(l/2)+9):
		#for i in range(32,41):
			for m in re.finditer(' ',letters):
				if(m.end() == i and flag == 0):
					#print("Iam2",flag)
					return letters[0:i-1] + "\n" + letters[i:]
					break

	return letters				
				#elif(m.end() == 36):
				#	return letters[0:36] + "\n" + letters[36:]
			#print(letters, m.start(),m.end())

for line in lines:
	line = line.strip()
	if(re.search(r' ',line)):
		length = len(line)
		if(length > 42):
			splitted_lines = findSpace(line)
			print(splitted_lines)
		else:
			print(line)
	else:
		print(line)



