# subtitle-aligner

## To Run(based on sentence aligned text)
```
python3 main2.py  -i FMFS-module-01-subtitle.srt -s=FMFS-module-01-transcription-clean-text.txt -t=FMFS-module-01-transcription-clean-text_eng_hin-postedited.txt > output.srt
```
### To use heuristics approach
```
python3 main2.py  -i FMFS-module-01-subtitle.srt -s=FMFS-module-01-transcription-clean-text.txt -t=FMFS-module-01-transcription-clean-text_eng_hin-postedited.txt -m=y > output.srt
```

## To Run(based on word count herutistics)
```
python3 main.py --t=FMFS-module-01-transcription-clean-text_eng_hin-postedited.txt -s=FMFS-module-01-subtitle.srt
```
output file will be created in output.srt

## To break each subtitle into two lines

python3 break_half.py output.srt
