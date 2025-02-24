#!/usr/env/python coding
# -*- coding: utf-8 -*-

## disambiguate.py
## Authors: C. Violand & J. Grasso
##

import re
import string

# SCHNEIDERS -->
# DiscourseConnective objects that qualify for a certain amount of 
# disambiguation confidence based on 1 of 3 disambiguation methods as 
# defined in "Bachelorarbeit_Angela_Schneider_735923".
schneider_ones = [('denn',['KON'],['ADV']),
					('doch',['KON'],['ADV']),
					('entgegen',['APPO','APPR'],['PTKVZ']),
					('seit',['KOUS'],['APPR']),
					('seitdem',['KOUS'],['PAV']),
					('trotz',['APPR'],['NN']),
					('während',['KOUS'],['APPR']),
					('wegen',['APPO','APPR'],['NN'])
					]

schneider_twos = ['also',
					'auch',
					'außer',
					'darum',
					'nebenher',
					'nur',
					'so',
					'sonst',
					'soweit',
					'zugleich'
					]

# Only case where there is no "all" involved.
schneider_two_special = ['da']

schneider_zeros = [('und',79),
					('als',17),
					('auch',1),
					('wie',12),
					('so',37),
					('nur',1),
					('aber',145),
					('dann',144),
					('doch',80),
					('da',90),
					('denn',116),
					('also',58),
					('seit',21),
					('während',102),
					('darauf',13),
					('dabei',19),
					('allein',17),
					('wegen',191),
					('dafür',22),
					('daher',184),
					('sonst',56),
					('statt',37),
					('zugleich',81),
					('allerdings',167),
					('dagegen',148),
					('ferner',182),
					('trotz',180),
					('darum',80),
					('außer',15),
					('soweit',169),
					('entgegen',58),
					('danach',115),
					('wonach',14),
					('worauf',97),
					('deshalb',76),
					('seitdem',61),
					('womit',91),
					('aufgrund',0),
					('allenfalls',23),
					('wogegen',146),
					('nebenher',107),
					('weswegen',89)
					]

# HANDLING FOR SCHNEIDERS TYPE '0'.
def disambiguate_remove_zeroes(dcons, zeros_limit = 0.8):		
	new_dcons = []
	for d in dcons:
		include = True	# all others added regardless
		for s in schneider_zeros:
			#schneider type 0 added only if in limit
			if (d.part_one[0].encode("utf-8") == s[0]) and ((200-s[1]) / float(200)) >= zeros_limit: 
				include = False
				### COMMENT OUT AFTER TESTING ###
				print "removing DC type 0 ", s[0]
				###
		if include:
			new_dcons.append(d)
			
	return new_dcons

def disambiguate(tweets, dcons):					
	# used to interpet the POS-tagged text files
	pattern = re.compile(r'[a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/[A-ZÄÖÜẞ]+')

	# PREPARATION FOR SCHNEDIERS TYPE '2'.		
	contexts = {
		'also' : [re.compile(r',\/,\/\$, [a-zA-ZäöüßÄÖÜẞ]+\/also\/ADV [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/VFIN'), 
				  re.compile(r'\.\/\.\/\$\. [a-zA-ZäöüßÄÖÜẞ]+\/also\/ADV [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/VFIN'),
				  re.compile(r'[a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/VFIN [a-zA-ZäöüßÄÖÜẞ]+\/also\/ADV')],
		'auch' : [re.compile(r'[a-zA-ZäöüßÄÖÜẞ]+\/auch\/ADV [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/VVFIN')],
		'außer': [re.compile(r'[\S]+\/[\S]+\/\$[\S]* [a-zA-ZäöüßÄÖÜẞ]+\/außer\/APPR ,\/,\/\$,'),
				  re.compile(r'[\S]+\/[\S]+\/\$[\S]* [a-zA-ZäöüßÄÖÜẞ]+\/außer\/APPR [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/KOUS')],
		'da' : [re.compile(r',\/,\/\$, [a-zA-ZäöüßÄÖÜẞ]+\/da\/ADV'),
				re.compile(r'[a-zA-ZäöüßÄÖÜẞ]+\/da\/KOUS'),
				re.compile(r'[\S]+\/[\S]+\/\$[\S]* [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/KON [a-zA-ZäöüßÄÖÜẞ]+\/da\/ADV')],
		'darum' : ["all"],
		'nebenher': ["all"],
		'nur' : [re.compile(r'\.\/\.\/\$\. [a-zA-ZäöüßÄÖÜẞ]+\/nur\/ADV [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/VVFIN')],
		'so' : [re.compile(r',\/,\/\$, [a-zA-ZäöüßÄÖÜẞ]+\/so\/ADV [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/KOUS'),
				re.compile(r',\/,\/\$, [a-zA-ZäöüßÄÖÜẞ]+\/so\/ADV [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/VFIN'),
				re.compile(r'[a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/KON [a-zA-ZäöüßÄÖÜẞ]+\/so\/ADV [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/VFIN')],
		'sonst' : [re.compile(r'[\S]+\/[\S]+\/\$[\S]* [a-zA-ZäöüßÄÖÜẞ]+\/sonst\/ADV [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/VFIN')],
		'soweit' : [re.compile(r'[a-zA-ZäöüßÄÖÜẞ]+\/soweit\/KOUS'),
					re.compile(r'[\S]+\/[\S]+\/\$[\S]* [a-zA-ZäöüßÄÖÜẞ]+\/soweit\/ADV')],
		'zugleich' : [re.compile(r'[a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/V[a-zA-ZäöüßÄÖÜẞ]* [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/KON [a-zA-ZäöüßÄÖÜẞ]+\/zugleich\/ADV'),
					  re.compile(r'[a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/VVFIN [a-zA-ZäöüßÄÖÜẞ]+\/zugleich\/ADV'),
					  re.compile(r'[\S]+\/[\S]+\/\$[\S]* [a-zA-ZäöüßÄÖÜẞ]+\/zugleich\/ADV [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/VFIN'),
					  re.compile(r'[\S]+\/[\S]+\/\$[\S]* [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/KON [a-zA-ZäöüßÄÖÜẞ]+\/zugleich\/ADV')]
		}

	not_contexts = {
		'also' : ["all"],
		'auch' : ["all"],
		'außer': ["all"],
		'da' : [re.compile(r' [a-zA-ZäöüßÄÖÜẞ]+\/da\/ADV' ),
				re.compile(r' [a-zA-ZäöüßÄÖÜẞ]+\/da\/PTKVZ' )],
		'darum' : [re.compile(r' [a-zA-ZäöüßÄÖÜẞ]+\/darum\/PAV [\S]+\/[\S]+\/\$\( [\S]+\/[\S]+\/\$[\S]*' ),
				   re.compile(r' [a-zA-ZäöüßÄÖÜẞ]+\/darum\/PAV ,\/,\/\$,' ),
				   re.compile(r' [a-zA-ZäöüßÄÖÜẞ]+\/darum\/PAV \.\/\.\/\$\.' ),
			   	   re.compile(r' [a-zA-ZäöüßÄÖÜẞ]+\/darum\/PAV [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/VV' )],
		'nebenher': [re.compile(r' [a-zA-ZäöüßÄÖÜẞ]+\/nebenher\/ADV [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/VVFIN' ),
					 re.compile(r' [a-zA-ZäöüßÄÖÜẞ]+\/nebenher\/ADV [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/VVPP' ),
					 re.compile(r' [a-zA-ZäöüßÄÖÜẞ]+\/nebenher\/ADV [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/KON' ),
					 re.compile(r' [a-zA-ZäöüßÄÖÜẞ]+\/nebenher\/ADV [a-zA-ZäöüßÄÖÜẞ]+\/[a-zA-ZäöüßÄÖÜẞ]+\/VVINF' ),
					 re.compile(r' [a-zA-ZäöüßÄÖÜẞ]+\/nebenher\/ADV [\S]+\/[\S]+\/\$[\S]*' )],
		'nur' : ["all"],
		'so' : ["all"],
		'sonst' : ["all"],
		'soweit' : ["all"],
		'zugleich' : ["all"]
		}

	# File handling for tweets-pos-tagged files.
	# Load file only when necessary, not during every iteration.
	current_file = {"name": None, "data": None}
	id_pattern = re.compile(r'^\t*(\d+)\t(.*)$')	
	
	def load_tagged_file(filename):
		if current_file["name"] != filename:
			data_dict = {}
			current_file["name"] = filename
			current_file["data"] = data_dict
			tagged_path = "../tweets-pos-tagged/" + t.filename + "-tagged.txt"
			tagged = open(tagged_path)
			for line in tagged:
				match = id_pattern.match(line)

				if match :
					id_num = match.group(1)		# groups defined by parenthesis in RE above, first is ID
					rest = match.group(2)		# next is rest of line	
					data_dict[id_num] = rest
					
		return current_file["data"]		
	
	for t in tweets:
		data = load_tagged_file(t.filename)
		line = data[t.id]
		
		# PREPARATION FOR SCHNEIDERS TYPE '1'.
		# Get dictionary of tagged words for current line of current tweet.
		results = re.findall(pattern,line)
		tagged_words = {}
		for i in results:
			parts = string.split(i,'/')
			if parts[1].lower() in tagged_words.keys():
				continue
			else:
				tagged_words[parts[1].lower()] = parts[2].lower()

		# DISAMBIGUATION PROCESS.		
		for x in t.dcs:
			# If DC occurance is cited as ambiguous.
			if x[1] == True:
				
				# HANDLING FOR SCHNEIDERS TYPE '1'.
				for j in range(len(schneider_ones)):			
					for k in tagged_words:
						if k == x[0].part_one[0].encode("utf-8"):
							if schneider_ones[j][0] == k:
								# Add to remove list if the part of speech matches the criteria for deletion.								
								if tagged_words[k] in [ i.lower() for i in schneider_ones[j][2] ]:
									t.dcs.remove(x)
									### COMMENT OUT AFTER TESTING ###
									print "removing DC type 1 ", x[0].part_one[0]
									###
									break							
								elif tagged_words[k][1] in schneider_ones[j][1]:
									pass
								else:
									# Remains ambiguous.
									t.ambis.append(x)
									### COMMENT OUT AFTER TESTING ###
									print "DC type 1 remains ambiguous ", x[0].part_one[0]
									###
							
				# HANDLING FOR SCHNEIDERS TYPE '2'.
				for l in schneider_twos:
					if x[0].part_one[0].encode("utf-8") == l:
						for q in not_contexts[l]:
							if re.search(q,line):
								t.dcs.remove(x)
								### COMMENT OUT AFTER TESTING ###
								print "removing DC type 2 ", x[0].part_one[0]
								###

				for l in schneider_two_special:
					if x[0].part_one[0].encode("utf-8") == l:
						flag = False
						for q in not_contexts[l]:
							if re.search(q,line):
								t.dcs.remove(x)
								### COMMENT OUT AFTER TESTING ###
								print "removing DC type 2 ", x[0].part_one[0]
								###
								flag == True
								break
								
						# Reason to keep.
						for p in contexts[l]:
							if re.search(p,line):
								flag == True
								break
						
						# Reason to add ambigous tag.
						if flag == False:
							# Remains ambiguous.
							t.ambis.append(x)
							### COMMENT OUT AFTER TESTING ###
							print "DC type 2 remains ambiguous ", x[0].part_one[0]
							###
							break								
										
		yield t

