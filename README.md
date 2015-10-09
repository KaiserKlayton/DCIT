```
Jessica Grasso
Universität Potsdam
MSc Program in Cognitive Systems
jgrasso@uni-potsdam.de
```
```
Clayton Violand
Universität Potsdam
MSc Program in Cognitive Systems
cvioland@uni-potsdam.de
```
# DCIT: Discourse Connectives in Twitter
DCIT is a tool written in Python that analyzes the usage of discourse connectives in German Twitter data. Given a list of German discourse markers and one or more files containing German-language tweets, the tool counts possible discourse connectives, performs disambiguation on the ambiguous connectives, and re-counts, printing a summary of the information collected and outputting annotated versions of the tweets.
## To run on (a) specific file(s):
$ python run.py a.xml b.xml
<br>
## To run on all files in ../tweets-xml/
$ python run.py glob
<br>
### NOTE 
```
From within ~/DCIT_Tool, the following is assumed:
1. Dimlex.html is in ../connectives-xml/dimlex.xml.
2. Tweet files are in ../tweets-xml/.
3. POS-tagged files are in ../tweets-pos-tagged/, having the same name as the tweet file w/ extension -tagged.txt.
4. Results are written to files with extension _new.xml and saved to ../results/, which is created if it does not exist.
```
