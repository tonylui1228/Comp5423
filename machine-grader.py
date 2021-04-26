# Aaron Martin
#
# Program that takes in answers created by the machine reader program and the correct answers and grades the accuracy of the results, marking how many were incorrect for each question and how many were correct total, and the accuracy
#
# Input:
# Machine answers:
# A C C B
# D B C A
# Correct answers:
# A C C D
# D A C D
# Output:
# A C C B | A C C D | 1
# D B C A | D A C D | 2
# Correct: 5
# Accuracy: .625
#
#	1. Read in answered and correct files
#	2. Parse each line (question)
#		a. Parse each answer
#			i. If answer is correct, add to total correct, else, add to total incorrect and incorrect for that question
#		b. Print question results
#	3. Calculate total correct and print
#	4. Calculate accuracy and print

import sys

def main(argv):

	# Read in and open files
	f1name = argv[1]
	f2name = argv[2]

	f1 = open(f1name, "r")
	f2 = open(f2name, "r")

	correct = 0
	incorrect = 0

	# For each line (question) in both files
	for ans, gold in zip(f1.readlines(), f2.readlines()):

		# Remove newline character
		ans = ans[:-1]
		gold = gold[:-1]

		# Split by individual answers
		anss = ans.split("\t")
		golds = gold.split("\t")

		incor = 0

		# For each answer
		for let, glet in zip(anss, golds):

			# If answered is the same as correct
			if(let == glet):
				correct += 1

			# If answer was incorrect
			else:
				incor += 1
				incorrect += 1

		print(ans, end="\t|\t")
		print(gold, end="\t|\t")
		print(incor)

	# Print total correct and calculated accuracy
	print("Num correct: ", correct)
	print("Accuracy: ", correct/(correct+incorrect))

	f1.close()
	f2.close()

main(sys.argv)
