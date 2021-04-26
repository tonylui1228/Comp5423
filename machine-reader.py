# Aaron Martin
# PA 6
#
# Program that takes in a file containing stories with associated questions, and attempts to answer those questions with different techniques involving the sliding window algorithm as well as other NLP utilities
#
# Input:
# <story> <question [answer] [answer] [answer] [answer]> <question...> ...
# Output:
# A C B B
# D A B C
# ...
#
#	1. Turn each line of the file into a Story object
#		a. Each story object is initialized with a field for the title, the text, and the question bank with answers
#			i. The text is removed of all unneccesary characters and symbols
#			ii. A word count dictionary is created against the story's text
#			iii. The question has the '?' removed
#	2. Parse each story
#		a. Parse each question attached to that story
#			i. Parse each answer associated with that question
#				- Calulcate window size based on word count of question and answer
#				- Read through story one window size of words at a time
#				- For each matching unique word, calculate that word's log score (log(1+(1/c(w)))) and add it to that window's score
#				- Which ever window has the highest score becomes that answer's final score
#			ii. Assign answer to question based on whichever answer has the highest score
#			iii. Print result

import sys
import math
import re
import nltk

# Story class
# Contains all information from individual line of test file
# Contains methods that can be used to aid in score calculation and information retrieval
class Story:

	# Initialze story object
	def __init__(self, data):

		# Remove symbols
		data = re.sub(r'[\?.\!,-]', '', data)

		# Split by tab and save to variables
		pieces = data.split("\t")

		self.title = pieces[0]

		self.stuff = pieces[1]

		self.text = pieces[2]
		# Text is also turned into a dictionary with word counts
		self.counts = self.counting()

		# Questions become a dictionary with the value being a list of answers
		self.qBank = {}

		self.qBank[pieces[3]] = [ pieces[4], pieces[5], pieces[6], pieces[7] ]
		self.qBank[pieces[8]] = [ pieces[9], pieces[10], pieces[11],  pieces[12] ]
		self.qBank[pieces[13]] = [ pieces[14], pieces[15], pieces[16], pieces[17] ] 
		self.qBank[pieces[18]] = [ pieces[19], pieces[20], pieces[21], pieces[22] ] 


	# Method for obtaining word counts
	def counting(self):

		l = self.text.split()

		countDict = {}

		for word in l:

			if word not in countDict.keys():
				countDict[word] = 1
			else:
				countDict[word] += 1

		return countDict

	# Method for caluclating score of word in story
	def logC(self, word):
		calc = math.log2(1 + ( 1 / self.counts[word] ) )
		return calc

	# Output method for testing purposes
	def output(self):
		print("Title: ", self.title)
		print("Extra content: ", self.stuff)
		print("Raw text: ", self.text)
		print("Dict and counts: ", self.counts)
		print("Question Bank: ", self.qBank)

# POS Tagging and question type checking
def checkPOSandQType(currentScore, q, a):

	aTokens = nltk.word_tokenize(a[0])
	tag = nltk.pos_tag(aTokens)[0][1]

	if "Who" in q:

		if tag == "NNP" or tag == "NNPS":
			currentScore += currentScore/2

	if "When" in q:

		if tag == "CD":
			currentScore += currentScore

	if "What" in q:

		if tag == "NN" or tag == "NNP" or tag == "NNPS":
			currentScore += currentScore/2


	return currentScore
		


def calculateScore(story, qAndA, mode, q, a):

	#Split story to list
	content = story.text.split()

	# Set size
	size = len(qAndA)

	# Make set
	qaSet = set(qAndA)

	# Score of the window with the max score
	maxScore = 0

	# Traverse story window size at a time
	for i in range(len(content) - size):

		# Make window
		window = content[i : i + size]

		#Score for this window
		score = 0

		# Traverse set and look for matches
		for word in qaSet:

			# If match, add to score
			if word in window:
				score += story.logC(word)

		# Adjust max score if its greater
		if score > maxScore:
			maxScore = score

	if mode == 1:
		maxScore = checkPOSandQType(maxScore, q, a)

	return maxScore

# Method for returning answer value based on answer with highest score
def maxOptions(scores):

	maxIndex = 0
	maxScore = 0

	# Find maximum score in scorecard array
	for i in range(4):
		if scores[i] > maxScore:
			maxScore = scores[i]
			maxIndex = i

	if maxIndex == 0:
		return 'A'
	if maxIndex == 1:
		return 'B'
	if maxIndex == 2:
		return 'C'
	if maxIndex == 3:
		return 'D'

	# If not found, default to A
	return 'A'

def answer(story, mode):

	# Traverse the questions in the story
	for i, key in zip(range(4), story.qBank.keys()):

		# Split question into list
		q = key.split()

		# Score keeping array
		# [ q1, q2, q3, q4 ]
		scores = [0, 0, 0, 0]

		# Traverse the possible answers
		for j, answer in zip(range(4), story.qBank[key]):

			# Split answer into list
			a = answer.split()

			# Make answer set to compare
			# [qword1, qword2, qword3, aword1, aword2 ]
			qAndA = q + a
			# Calculate that answer's score, and place on scorecard array
			scores[j] = calculateScore(story, qAndA, mode, q, a)

		# Choose max score option
		# Print result
		print(maxOptions(scores), end="")

		# Formatting print statements
		if i < 3:
			print("\t", end="")
		else:
			print()

def main(argv):
 
	# Read in mode and filepath
	mode = argv[1]
	fname = argv[2]

	# Open test file
	f = open(fname, "r")

	# Array for holding each story object
	data = []

	# Read in story line and remove newline character
	for l in f.readlines():
		data.append(Story(l[:-1]))

	f.close()

	# Answer questions from each story
	for story in data:
		answer(story, int(mode))

main(sys.argv)
