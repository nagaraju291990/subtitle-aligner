#This script generates hindi/telugu subtitle file from parallel translated files using eng srt file
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
parser.add_argument("-m", "--method heuristic", dest="h",
                    help="Use heuristic approach -h=y",required=False)

args = parser.parse_args()

inputfile = args.inputfile
sourcefile = args.sourcefile
targetfile = args.targetfile
h = args.h

if(h is None):
	h = 'nd '
else:
	h = h.lower()

new_line = []
new_line2 = []
timeline = []
timeline_hash = {}
src_tgt_hash = {}
final_out = []

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
		s = re.sub(r'[\-,\.\'\"\-]', "", s)
		s = s.strip()
		t = t.strip()
		s = re.sub(r'\s+',' ', s)
		s = re.sub(r'^ ', '', s)
		s = re.sub(r' $', '', s)
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
		sub_placeholder2 = "##" + str(count) + ""
		sub_placeholder = str(sub.start) + " --> " + str(sub.end)
		timeline_hash[sub_placeholder2] = str(sub.start) + " --> " + str(sub.end)
		#new_line.append("[" + str(sub.start) + " --> " + str(sub.end) + "]")
		new_line.append(sub_placeholder)
		new_line.append(cur_text)
		new_line2.append(sub_placeholder2)
		new_line2.append(cur_text)
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
				st = re.sub(r'[\-,\.\'\"\-]', "", st)
				st = st.strip()
				st = re.sub(r'\s+',' ', st)
				st = re.sub(r'^ ', '', st)
				st = re.sub(r' $', '', st)
				if(st in src_tgt_hash):
					print(src_tgt_hash[st],end='')
				else:
					print(sentence, end='')
			print("\n")

def alignSRT2():
	count = 1
	#print(new_line)
	eng_sub = ' '.join(new_line2)
	eng_sub = re.sub(r'MUSIC', 'MUSIC.', eng_sub)
	#print(eng_sub)
	sentences = nltk.tokenize.sent_tokenize(eng_sub)
	#sentences = eng_sub.split("]")
	count = 1
	#print(sentences)
	for s in sentences:
		s = s.lower()
		#print(s)
		
		if(1):
			s_original = s
			indices = re.finditer(r'##\d+', s)
			s = re.sub(r'##\d+', '', s)

			s_tmp = s
			s = re.sub(r'[\-,\.\'\"\-]', "", s)
			s = s.strip()
			s = re.sub(r'\s+',' ', s)
			s = re.sub(r'^ ', '', s)
			s = re.sub(r' $', '', s)
			#print(s)
			if(s == "music."):
				s = "music"

			
			if(s in src_tgt_hash):
				#print("Im ahre")
				s_trans = src_tgt_hash[s]
			else:
				s_trans = s_tmp

			space_split = s_original.split(" ")
			space_split_trans = s_trans.split(" ")
			#print("Iam ", s_original)
			if(re.search(r'##\d+', s_original)):
				for i in indices:

					#print(i, s_original)
					if(i is None):
						final_trans = ' '.join(space_split_trans)
						break
					#print(space_split_trans, "ii")
					insert_ph = i.group()
					char_index = i.start()
					
					#s_trans = s_trans[:char_index] + insert_ph + s_trans[char_index:]
					word_index = space_split.index(insert_ph)
					insert_ph = timeline_hash[insert_ph]
					space_split_trans.insert(word_index,  insert_ph)
					#final_trans = '\n' + str(count) + '\n' + ' '.join(space_split_trans) 
					final_trans = ' '.join(space_split_trans) 
					count = count + 1
					final_trans = re.sub(r' +', ' ', final_trans)
					#print("1",final_trans)
					#print(s, i.start(), i.group())
					#final_trans = re.sub(r'(\n)+', '\n', final_trans)
				final_out.append(final_trans)
			else:
				#print("")
				#print(s_trans +"\n")
				final_out.append(s_trans)
		else:
			print(s+"\n")
def printhash():
	for k in src_tgt_hash:
		outfp.write(k + "\t" + src_tgt_hash[k] + "\n")

srctgthash(sourcefile, targetfile)
extractTextFromSRT(inputfile)
if(h == 'y'):
	alignSRT2()
else:
	alignSRT()
#print(final_out)


count = 1
for p in final_out:
	#p = re.sub(r'[^>] (\d)', r'\n\n\1', p)
	#p = re.sub(r'--> (\d\d:\d\d:\d\d,\d\d\d)', r'--> \1\n', p)

	mall = re.split(r'(\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d)', p)
	for m in mall:
		if(m):
			if(re.search(r'\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d', m)):
				if(count == 1):
					print(count)
				else:
					print("\n",count)
				count = count + 1
			print(m)
	#print(p + "\n")
printhash()
#print(timeline_hash)
#exit(0)
