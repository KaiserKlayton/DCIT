#!/usr/bin/env python
# -*- coding: utf-8 -*-

## get_matches.py
## Authors: C. Violand & J. Grasso
##

import re
from collections import Counter

def get_matches(tweets, dcons, info):
	tweet_trigger = False
	discontins = [i for i in dcons if i.sep == "discont"]
	contins = [i for i in dcons if i.sep == "cont"]
	
	for t in tweets:
		info.tweets += 1	# number of Tweets seen so far
		tweet_trigger = False
	
		# DISCONTINUOUS CASES
		for i in discontins:
			for j in range(len(i.ortho_blocks)):
				if '.' in i.part_one[j]:
					i.part_one[j] = i.part_one[j].replace('.', '')
				if '.' in i.part_two[j]:
					i.part_two[j] = i.part_two[j].replace('.', '')
				if i.type_part_one[j] == "phrasal" and i.type_part_two[j] == "single":
					index = 0
					copy = t._original.lower()
					while bool(re.search(r"\b%s\b" % i.part_one[j], t.raw)) and bool(re.search(r"\b%s\b" % i.part_two[j], t.raw)) and t.raw.find(i.part_one[j]) < t.raw.find(i.part_two[j]):	
						### COMMENT OUT AFTER TESTING ###
						print "Found a DC (phrasal-single)!"
						###
						tweet_trigger = True
						# Update count of discontinuous DCs.
						info.discontinuous += 1
						info.discontinuous_dict[i] += 1
						
						# Remove found cases.
						t.raw = t.raw.replace(i.part_one[j], '', 1)
						t.raw = t.raw.replace(i.part_two[j], '', 1)

						# Check for potential ambiguity and update Tweet object.
						a = (i.ambi=='1')						
						if a:
							t.has_ambi_dc = True
							t.ambi_count_discontins += 1
							info.ambiguous_dict[i] += 1
						b = copy.replace(i.part_one[j], '%s' % ('X' * len(i.part_one[j])), index).find(i.part_one[j])
						index += 1
						t.dcs.append((i,a,b))

				# Check for the alternate scenario (where type_part_one is 
				# single and type_part_two is phrasal.
				elif i.type_part_one[j] == "single" and i.type_part_two[j] == "phrasal":
					index = 0
					copy = t._original.lower()
					while bool(re.search(r"\b%s\b" % i.part_one[j], t.raw)) and bool(re.search(r"\b%s\b" % i.part_two[j], t.raw)) and t.raw.find(i.part_one[j]) < t.raw.find(i.part_two[j]):
						### COMMENT OUT AFTER TESTING ###
						print "Found a DC (single-phrasal)!"
						###
						tweet_trigger = True
						# Update count of discontinuous DCs.
						info.discontinuous += 1
						info.discontinuous_dict[i] += 1
						
						# Remove found cases.
						t.raw = t.raw.replace(i.part_one[j], '', 1)
						t.raw = t.raw.replace(i.part_two[j], '', 1)

						# Check for potential ambiguity and update Tweet object.
						a = (i.ambi=='1')						
						if a:
							t.has_ambi_dc = True
							t.ambi_count_discontins += 1
							info.ambiguous_dict[i] += 1
						b = copy.replace(i.part_one[j], '%s' % ('X' * len(i.part_one[j])), index).find(i.part_one[j])
						index += 1
						t.dcs.append((i,a,b))

				# Check for the last alternate scenario.
				elif i.type_part_one[j] == "single" and i.type_part_two[j] == "single":
					index = 0
					copy = t._original.lower()
					while bool(re.search(r"\b%s\b" % i.part_one[j], t.raw)) and bool(re.search(r"\b%s\b" % i.part_two[j], t.raw)) and t.raw.find(i.part_one[j]) < t.raw.find(i.part_two[j]):
						### COMMENT OUT AFTER TESTING ###
						print "Found a DC (single-single)!"
						###
						tweet_trigger = True
						# Update count of discontinuous DCs.
						info.discontinuous += 1
						info.discontinuous_dict[i] += 1

						# Remove found cases.
						t.raw = t.raw.replace(i.part_one[j], '', 1)
						t.raw = t.raw.replace(i.part_two[j], '', 1)
						
						# Check for potential ambiguity and update Tweet object.
						a = (i.ambi=='1')						
						if a:
							t.has_ambi_dc = True
							t.ambi_count_discontins += 1	
							info.ambiguous_dict[i] += 1
						b = copy.replace(i.part_one[j], '%s' % ('X' * len(i.part_one[j])), index).find(i.part_one[j])
						index += 1
						t.dcs.append((i,a,b))

		# CONTINUOUS CASES
		for i in contins:
			for j in range(len(i.ortho_blocks)):
				if '.' in i.part_one[j]:
					i.part_one[j] = i.part_one[j].replace('.', '')
				if i.type_part_one[j] == "phrasal":
					index = 0
					copy = t._original.lower()
					while bool(re.search(r"\b%s\b" % i.part_one[j], t.raw)):
						tweet_trigger = True
						### COMMENT OUT AFTER TESTING ###
						print "Found a DC (phrasal)!"
						###
						# Update count of discontinuous DCs.
						info.continuous += 1
						info.continuous_dict[i] += 1

						# Remove found cases.
						t.raw = t.raw.replace(i.part_one[j], '', 1)
					
						# Check for potential ambiguity and update Tweet object.
						a = (i.ambi=='1')
						if a:
							t.has_ambi_dc = True
							t.ambi_count_contins += 1
							info.ambiguous_dict[i] += 1
						b = copy.replace(i.part_one[j], '%s' % ('X' * len(i.part_one[j])), index).find(i.part_one[j])
						index += 1
						t.dcs.append((i,a,b))

				# Check for alternate Scenario.
				if i.type_part_one[j] == "single":
					index = 0
					copy = t._original.lower()
					while bool(re.search(r"\b%s\b" % i.part_one[j], t.raw)):
						tweet_trigger = True
						### COMMENT OUT AFTER TESTING ###
						print "Found a DC (single)!"
						###
						# Update count of discontinuous DCs.
						info.continuous += 1
						info.continuous_dict[i] += 1	

						# Remove found cases.
						t.raw = t.raw.replace(i.part_one[j], '', 1)

						# Check for potential ambiguity and update Tweet object.
						a = (i.ambi=='1')
						if a:
							t.has_ambi_dc = True
							t.ambi_count_contins += 1
							info.ambiguous_dict[i] += 1					
						b = copy.replace(i.part_one[j], '%s' % ('X' * len(i.part_one[j])), index).find(i.part_one[j])
						index += 1
						t.dcs.append((i,a,b))

		if tweet_trigger == True:
			info.tweets_with_dcs += 1
	
		info.discontinuous_ambi += t.ambi_count_discontins
		info.continuous_ambi += t.ambi_count_contins

		yield t

