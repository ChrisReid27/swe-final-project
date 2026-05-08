from .serializers import QuestionSerializer
import json
import random

import logging

logger = logging.getLogger(__name__)

def _pick_random(bucket, bucket_name):
	if not bucket:
		raise ValueError(f'No questions available for {bucket_name}.')
	return random.choice(bucket)

def chooseRandomFive(listoflists):
	# first choose a howard related question
	skip = 0
	returnlist = [0, 0, 0, 0, 0]
	
	howard_question = _pick_random(listoflists[5], 'Howard bucket')
	val = howard_question[0]
	returnlist[val] = howard_question[1]

	for i in range(5):
		if(i == val):
			continue
		else:
			question = _pick_random(listoflists[i], f'value bucket {i + 1}')
			returnlist[i] = question
	
	return returnlist

# generate a random board from a JSON of all the questions 
def createNewBoard(questions):
	question_list = []
	for entry in questions:
		question_list.append({'howard' : entry.howard, 'category' : entry.category, 'value' : entry.value})

	# add a number value to identify the questions by
	i = 0

	# buckets for each of the values (the sixth bucket is the howard bucket)
	movies = [ [] for _ in range(6) ]
	sports = [ [] for _ in range(6) ]
	tv = [ [] for _ in range(6) ]
	celebrities = [ [] for _ in range(6) ]
	music = [ [] for _ in range(6) ]
	
	for question in question_list:
		# split the data up into category and value buckets
		val = question['value']
		val = int(val / 200) - 1

		if question['howard'] is True:
			identifier = (val, i)
			val = 5
		else:
			identifier = i	

		category = question['category']
		if category == 'movies':
			movies[val].append(identifier)
		elif category == 'sports':
			sports[val].append(identifier)
		elif category == 'tv':
			tv[val].append(identifier)
		elif category == 'celebrities':
			celebrities[val].append(identifier)
		elif category == 'music':
			music[val].append(identifier)

		i += 1

	movies_list = chooseRandomFive(movies)
	sports_list = chooseRandomFive(sports)
	tv_list = chooseRandomFive(tv)
	celebrities_list = chooseRandomFive(celebrities)
	music_list = chooseRandomFive(music)
	
	total_list = movies_list + sports_list + tv_list + celebrities_list + music_list
	return_list = []
	# now get the corresponding question object for each question_index in the list
	for question_index in total_list:		
		return_list.append(questions[question_index])

	return return_list
