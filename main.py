#subtitle alignment of a translated file w.r.t to english subtitle file

import sys
import re
from argparse import ArgumentParser
import pysrt
import math

parser = ArgumentParser(description='This script will align Subtitle translation files\n\r'+
						"How to Run?\n" +
						"python3 " + sys.argv[0] + " -t=trans-inputfie.txt" + " -s=subtitle.srt -e=eng.txt"
						)

parser.add_argument("-t", "--translation", dest="transfile",
					help="provide .txt translated file name",required=True)
parser.add_argument("-s", "--subtitle", dest="srtfile",
					help="specify .srt file", required=True)
#parser.add_argument("-e", "--engfile", dest="engfile",
#					help="specify english file.txt", required=True)

args = parser.parse_args()

transfile = args.transfile	##input file
srtfile = args.srtfile		##srt file
#engfile = args.engfile		#original english file

with open(transfile) as fp:
	tlines = fp.read()#.split(" ")

tlines = re.sub(r'\n', ' ', tlines, flags=re.MULTILINE)
tlines = re.sub(r' +', ' ', tlines, flags=re.MULTILINE)
tlines = re.sub(r'^ ', '', tlines, flags=re.MULTILINE)
tlines = re.sub(r' $', '', tlines, flags=re.MULTILINE)
input_lines = tlines.split(" ")
tlines = re.sub(r' ?\| ?', '|', tlines, flags = re.MULTILINE)
tlines = re.sub(r'\(\(.+?\)\)', lambda x:x.group().replace(" ","####"), tlines)
input_lines = tlines.split(" ")
#tlines = re.sub(r' (के) ', r'####\1####', tlines, flags=re.MULTILINE)
#tlines = re.sub(r' (की) ', r'####\1 ', tlines, flags=re.MULTILINE)
#tlines = re.sub(r' ([\u0900-\u09FF][\u0900-\u09FF]) ', r'####\1####', tlines, flags=re.MULTILINE)


lines = tlines.split(" ")
#print(lines)
subs = pysrt.open(srtfile)

#with open(engfile) as fp:
#	elines = fp.read().split("\n")

#outfp = open(transfile + "_paralle.srt","w")
outfp = open("output.srt","w")
count = 1
i = 0
subs_text = subs.text
subs_text_lines = re.sub(r'\n',' ', subs_text, flags = re.MULTILINE)
subs_lines = subs_text_lines.split(" ")
#print(len(subs_lines),len(input_lines))
factor = math.ceil(len(input_lines)/len(subs_lines))
#factor = str(round(factor,2))
#print(factor)
subs_text_words = subs_text_lines.split(" ")
subs_count = len(subs)

for sub in subs:
	timeline_start = str(sub.start)
	timeline_end = str(sub.end)
	cur_text = sub.text
	noofwords = len(cur_text.split(" "))
	if(count%2 == 0):
		#print(count)
		out_words = lines[int(i):int(i+noofwords+factor)]
		i = i + noofwords + factor
	else:
		out_words = lines[int(i):int(i+noofwords+factor)]
		i = i + noofwords + factor
	#print(i)
	outfp.write(str(count) + "\n")
	outfp.write(str(sub.start) + " --> " + str(sub.end) +"\n")
	if(count == subs_count):
		out_words = lines[int(i):]
	out_lines = ' '.join(out_words)
	out_lines = re.sub(r'####',' ', out_lines, flags = re.MULTILINE)
	outfp.write(out_lines + "\n\n")
	#outfp.write
	count = count + 1

