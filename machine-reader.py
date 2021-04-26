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

        self.qBank[pieces[3]] = [pieces[4], pieces[5], pieces[6], pieces[7]]
        self.qBank[pieces[8]] = [pieces[9], pieces[10], pieces[11], pieces[12]]
        self.qBank[pieces[13]] = [pieces[14], pieces[15], pieces[16], pieces[17]]
        self.qBank[pieces[18]] = [pieces[19], pieces[20], pieces[21], pieces[22]]

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
        calc = math.log2(1 + (1 / self.counts[word]))
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
            currentScore += currentScore / 2

    if "When" in q:

        if tag == "CD":
            currentScore += currentScore

    if "What" in q:

        if tag == "NN" or tag == "NNP" or tag == "NNPS":
            currentScore += currentScore / 2

    return currentScore


def get_score(story, q_a, q, a):
    content = story.text.split()
    size = len(q_a)
    q_a = set(q_a)
    max_score = 0
    for i in range(len(content) - size):
        window = content[i: i + size]
        score = 0
        for word in q_a:
            if word in window:
                score += story.logC(word)

        if score > max_score:
            max_score = score

    max_score = checkPOSandQType(max_score, q, a)

    return max_score


# Method for returning answer value based on answer with highest score
def max_options(scores):
    if max(scores) == scores[0]:
        return 'A'
    if max(scores) == scores[1]:
        return 'B'
    if max(scores) == scores[2]:
        return 'C'
    if max(scores) == scores[3]:
        return 'D'
    return 'A'


def find_answer(story):
    for i, key in zip(range(4), story.qBank.keys()):
        q = key.split()
        scores = [0, 0, 0, 0]

        for j, answer in zip(range(4), story.qBank[key]):
            a = answer.split()
            qAndA = q + a
            scores[j] = get_score(story, qAndA, q, a)

        print(max_options(scores), end="")

        if i < 3:
            print("\t", end="")
        else:
            print()


def do_test(file):
    file = open(file, "r")
    data = []
    for line in file.readlines():
        data.append(Story(line[:-1]))
    file.close()
    for story in data:
        find_answer(story)


# do_test('data/MCTest/mc160.test.tsv')
do_test('data/MCTest/mc500.test.tsv')
