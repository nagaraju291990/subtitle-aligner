#This script generates hindi/telugu subtitle file from parallel translated files using eng srt file
from argparse import ArgumentParser
import re
import os
import sys
import pysrt
import nltk
import logger as log

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
parser.add_argument("-l", "--lang", dest="lang",
					help="provide 3 letter language code", required=False)
parser.add_argument("-m", "--method heuristic", dest="h",
                    help="Use heuristic approach -h=y",required=False)

log.logging.info("Parsing command line arguments")

args = parser.parse_args()

inputfile = args.inputfile
sourcefile = args.sourcefile
targetfile = args.targetfile
lang = args.lang
h = args.h

log.logging.info("Received following arguments: inputfile=%s, source file=%s, target file=%s, lang=%s" %(inputfile, sourcefile, targetfile, lang))

if(h is None):
	h = 'y'
else:
	h = h.lower()

new_line = []
new_line2 = []
timeline = []
timeline_hash = {}
src_tgt_hash = {}
final_out = []

outfp = open("tmp_hash.txt","w")
outfp1 = open("not_substituted.txt", "w")

def srctgthash(s,t):
	with open(s) as fp1:
		slines = fp1.read().split("\n")
	with open(t) as fp2:
		tlines = fp2.read().split("\n")
	#print(len(slines),len(tlines))
	l1 = len(slines)
	l2 = len(tlines)
	if(l1 != l2):
		log.logging.info("Exiting because source file and target file line numbers mismatched.")
		print("Source file and target file line numbers mismatch!")
		exit()
	for s, t in zip(slines, tlines):
		s = re.sub(r'(\d+)\.(\d+)', r'\1#DOT\2', s)
		#print(s,t)
		s = re.sub(r'[\-,\.\'\"\-]', " ", s)
		s = s.strip()
		t = t.strip()
		s = re.sub(r'\s+',' ', s)
		t = re.sub(r' ?\| ?', '|', t, flags = re.MULTILINE)
		t = re.sub(r'\(\(.+?\)\)', lambda x:x.group().replace(" ","####"), t)
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
		cur_text = re.sub(r'(\d+)\.(\d+)', r'\1#DOT\2', cur_text)
		cur_text = re.sub(r'([\-,\.\'\"\-])', r"\1 ", cur_text)
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
			count = count + 1
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
					t = src_tgt_hash[st]
					t = re.sub(r'####', ' ', t)
					print(t, end='')
				else:
					print(sentence, end='')
			print("\n")

def alignSRT2():
	count = 1
	#print(new_line)
	eng_sub = ' '.join(new_line2)
	eng_sub = re.sub(r'\[?MUSIC\]?', 'MUSIC.', eng_sub, flags=re.IGNORECASE)
	#print(eng_sub)
	sentences = nltk.tokenize.sent_tokenize(eng_sub)
	log.logging.info("After tokenization of english sentences, sent=%s" %('\n'.join(sentences)))
	#sentences = eng_sub.split("]")
	count = 1
	if(lang == "tel"):
		words = ['the', 'in', 'a', 'that', 'to', 'as', 'into', 'at']
	else:
		words = []
	#print(sentences)
	for s in sentences:
		s = s.lower()

		log.logging.info("Current sentence after lower case=%s" %(s))
		#print(s)
		
		if(1):
			s_original = s
			s = re.sub(r'(\d+)\.(\d+)', r'\1#DOT\2', s)
			indices = re.finditer(r'##\d+', s)
			s = re.sub(r'##\d+', '', s)

			s_tmp = s
			s = re.sub(r'[\-,\.\'\"\-]', " ", s)
			s = s.strip()
			s = re.sub(r'\s+',' ', s)
			s = re.sub(r'^ ', '', s)
			s = re.sub(r' $', '', s)
			#print(s)
			if(s == "music."):
				s = "music"

			
			#print("hello"+s)
			if(s in src_tgt_hash):
				#print("Im ahre")
				s_trans = src_tgt_hash[s]
			else:
				write_out = re.sub(r' +', ' ', s_tmp)
				outfp1.write(write_out + "\n")
				outfp1.write(s_original + "\n")
				s_trans = s_tmp
			log.logging.info("After finding in hash target text=%s" %(s_trans))
			#print(s_original)
			for w in words:
				s_original = re.sub(r' '+w+' ', ' ', s_original)
			#print(s_original)
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
					#print(insert_ph, char_index)
					#s_trans = s_trans[:char_index] + insert_ph + s_trans[char_index:]
					word_index = space_split.index(insert_ph)
					insert_ph = timeline_hash[insert_ph]
					target_index = word_index-1
					if(target_index < 0):
						target_index = 0
					space_split_trans.insert(target_index,  insert_ph)
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

log.logging.info("Going to making hash from source file and target file")
srctgthash(sourcefile, targetfile)
log.logging.info("Going to extract text from srt file")
extractTextFromSRT(inputfile)
log.logging.info("After text extraction from srt, text=%s" %("\n".join(new_line2)))
if(h == 'y'):
	log.logging.info("Going into align function")
	alignSRT2()
else:
	alignSRT()
#print(final_out)


count = 1
for p in final_out:
	p = re.sub(r'####', ' ', p)
	#p = re.sub(r'[^>] (\d)', r'\n\n\1', p)
	#p = re.sub(r'--> (\d\d:\d\d:\d\d,\d\d\d)', r'--> \1\n', p)

	mall = re.split(r'(\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d)', p)
	for m in mall:
		m = re.sub(r' +', ' ', m)
		m = re.sub(r'^ ', '', m)
		m = re.sub(r' $', '', m)
		if(m):
			if(re.search(r'\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d', m)):
				if(count == 1):
					print(count)
				else:
					print("\n", count, sep='')
				count = count + 1
			print(m)
	#print(p + "\n")
printhash()
#print(timeline_hash)
#exit(0)
outfp.close()
outfp1.close()