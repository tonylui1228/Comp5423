import sys
import math
import re
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


# article class
# Contains all information from individual line of test file
# Contains methods that can be used to aid in score calculation and information retrieval
class Article:

    # Initialze article object
    def __init__(self, data):

        # Remove symbols
        data = re.sub(r'[\?.\!,-]', '', data)

        # Split by tab and save to variables
        seg = data.split("\t")

        self.title = seg[0]

        self.stuff = seg[1]

        self.text = seg[2]
        # Text is also turned into a dictionary with word counts
        self.counts = self.counting()

        # Questions become a dictionary with the value being a list of answers
        self.qRepo = {}

        self.qRepo[seg[3]] = [seg[4], seg[5], seg[6], seg[7]]
        self.qRepo[seg[8]] = [seg[9], seg[10], seg[11], seg[12]]
        self.qRepo[seg[13]] = [seg[14], seg[15], seg[16], seg[17]]
        self.qRepo[seg[18]] = [seg[19], seg[20], seg[21], seg[22]]

    # Method for obtaining word counts
    def counting(self):

        p = self.text.split()

        countDict = {}

        for word in p:

            if word not in countDict.keys():
                countDict[word] = 1
            else:
                countDict[word] += 1

        return countDict

    # Method for caluclating score of word in article
    def logC(self, word):
        calc = math.log2(1 + (1 / self.counts[word]))
        return calc

    def output(self):
        print("Title: ", self.title)
        print("Extra content: ", self.stuff)
        print("Raw text: ", self.text)
        print("Dict and counts: ", self.counts)
        print("Question Repository: ", self.qRepo)


# POS Tagging and question type checking
def checkPOSandQType(Score, ques, ans):
    Token = nltk.word_tokenize(ans[0])
    tag = nltk.pos_tag(Token)[0][1]

    if "Who" in ques:
        if tag == "NNP" or tag == "NNPS":
            Score += Score / 2

    if "When" in ques:
        if tag == "CD":
            Score += Score

    if "What" in ques:
        if tag == "NN" or tag == "NNP" or tag == "NNPS":
            Score += Score / 2

    return Score

# map score to 'A' or 'B' or 'C' or 'D'
def find_mc_answer(scores):
    if max(scores) == scores[0]:
        return 'A'
    if max(scores) == scores[1]:
        return 'B'
    if max(scores) == scores[2]:
        return 'C'
    if max(scores) == scores[3]:
        return 'D'
    return 'A'

# get the score of a question answer
def get_score(article, question, answer):
    article_text = article.text.split()

    question_and_answer = question + answer
    # find the window size base on the length of the question and answer
    window_size = len(question_and_answer)
    # convert to set to avoid repeat text
    question_and_answer = set(question_and_answer)
    max_score = 0
    # use sliding window method to calculate the score for each answer
    for i in range(len(article_text) - window_size):
        score = 0
        # find sliding window base on the index
        sliding_window = article_text[i: i + window_size]
        for word in question_and_answer:
            # find if the word inside the question and answer exis at the sliding window
            if word in sliding_window:
                score += article.logC(word)
        if score > max_score:
            max_score = score

    max_score = checkPOSandQType(max_score, question, answer)
    return max_score


# find answer of all question inside a article
def find_answer(article):
    ans = ""
    i = 0
    # loop though all article
    for key in article.qRepo.keys():
        question = key.split()
        scores = []

        # find score for each question
        for answer in article.qRepo[key]:
            answer = answer.split()
            scores.append(get_score(article, question, answer))

        # find answer base on the score
        ans += find_mc_answer(scores)
        if i < 3:
            ans += "\t"
        i += 1
    return ans + "\n"


def do_test(file):
    file = open(file, "r")
    data = []
    # read test data
    for line in file.readlines():
        line = line[:-1]
        data.append(Article(line))
    file.close()

    # write answer data
    out = open('ans.txt', 'w')
    for article in data:
        out.write(find_answer(article))


do_test('data/MCTest/mc500.test.tsv')
