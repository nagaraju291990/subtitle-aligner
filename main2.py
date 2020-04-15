#This script converts srt file into text format like text.....[SUB____1]....text [SUB____2]
#and also generates a timeline file required later for processing
from argparse import ArgumentParser
import re
import os
import sys
import pysrt
import nltk

parser = ArgumentParser(description='This script will align Subtitle translation files\n\r'+
						"How to Run?\n" +
						"python3 " + sys.argv[0] + " -i=input.srt" + " -s=srctext.txt -t=target.txt"
						)
parser.add_argument("-i", "--input", dest="inputfile",
                    help="provide .srt file name",required=True)
parser.add_argument("-s", "--source", dest="sourcefile",
                    help="provide sentence aligned source file",required=True)
parser.add_argument("-t", "--target", dest="targetfile",
                    help="provide sentence aligned target file",required=True)
args = parser.parse_args()

inputfile = args.inputfile
sourcefile = args.sourcefile
targetfile = args.targetfile

new_line = []
timeline = []
timeline_hash = {}
src_tgt_hash = {}

outfp = open("tmp_hash.txt","w")

def srctgthash(s,t):
	with open(s) as fp1:
		slines = fp1.read().split("\n")
	with open(t) as fp2:
		tlines = fp2.read().split("\n")
	#print(len(slines),len(tlines))
	l1 = len(slines)
	l2 = len(tlines)
	if(l1 != l2):
		print("Source file and target file line numbers mismatch!")
		exit()
	for s, t in zip(slines, tlines):
		#print(s,t)
		s = s.strip()
		t = t.strip()
		src_tgt_hash[s.lower()] = t

def extractTextFromSRT(i):

	srtfilename = i
	subs = pysrt.open(srtfilename)
	ts_start = []
	ts_end = []
	remaining_text = ''
	front_text = ''
	#print(subs)
	count = 1
	for sub in subs:
		timeline_start = str(sub.start)
		timeline_end = str(sub.end)
		cur_text = sub.text
		cur_text = re.sub(r'\n', ' ' ,cur_text)
		#sub_placeholder = "[SUB____" + str(count) + "]"
		sub_placeholder = str(sub.start) + " --> " + str(sub.end)
		#timeline_hash[sub_placeholder] = str(sub.start) + " --> " + str(sub.end)
		#new_line.append("[" + str(sub.start) + " --> " + str(sub.end) + "]")
		new_line.append(sub_placeholder)
		new_line.append(cur_text)
		#new_line[-1] = new_line[-1].strip() + cur_text
		count = count + 1

def alignSRT():
	count = 1
	#print(count)
	for line in new_line:
		if(re.search(r'-->',line)):
			print(count)
			count = count + 1
			print(line)
		else:
			sentences = nltk.tokenize.sent_tokenize(line)		
			for sentence in sentences:
				st = sentence.lower()
				if(st in src_tgt_hash):
					print(src_tgt_hash[st],end='')
				else:
					print(sentence, end='')
			print("\n")
			#print(line)
		#if(count%2 == 0):
			#count = count + 1
			#print(count)

def printhash():
	for k in src_tgt_hash:
		outfp.write(k + "\t" + src_tgt_hash[k] + "\n")

srctgthash(sourcefile, targetfile)
extractTextFromSRT(inputfile)
alignSRT()
printhash()
#print(timeline_hash)
#exit(0)

count = 1
for line in new_line:
	#print(count)
	line = re.sub(r']', '] ',line)
	#line = re.sub(r'\.', '.\n' ,line)
	#line = line.strip()
	#print(line, end='')
	#print(line)
	count = count + 1
