from random import choice
import copy
import random

punc_list = (".", ",", "?", "!", ";", ":")
structure_types = ('~N','~J')

def split(message):
    new_message = ''
    for c in message:
        if c in punc_list:
            new_message += ' '
        new_message += c
    return new_message.split()

class generator:
    #For every word, maps the word to possible parts of speech.
    dictionary = {}
    
    grammar = {}

    #Scale back the dictionary to only include the 10k most used words, and only common usages.
    '''Every words is associated with at least one part of speech. The abbreviations are as follows:
    *N: noun
    T: transitive verb
    V: intransitive verb
    H: helper verb
    L: linking verb
    *J: adjective
    D: adverb
    C: conjunction
    P: pronoun
    I: interjection
    R: preposition
    S: spoken contraction
    E: determiners
    '''
    grammar_frame = {
        "~STRUCTURE": [
            ["~NOUNP", "~VERBP"],
            ["~NOUNP", "~VERBP", "~C", "~NOUNP", "~VERBP"],
        ],
        "~SENTENCE": [],
        "~NOUNP": [
            ["~E", "~J", "~N"],
        ],
        "~E": [],
        "~N": [],
        "~VERBP": [
            ["~T", "~NOUNP"],
            ["~V"],
        ],
        "~T": [],
        "~V": [],
        "~H": [],
        "~L": [],
        "~I": [],
        "~R": [],
        "~S": [],
        "~C": [],
        "~J": [],
        "~D": [],
        "~P": [],
    }

    grammar_default = {
        "~N": [
            ["pencil"], ["card"], ["tree"], ["book"], ["sand"], ["waves"]
        ],
        "~V": [
            ["sneezed"], ["grow"], ["runs"]
        ],
        "~T": [
            ["throws"], ["makes"], ["destroy"], ["counted"], ["have"]
        ],
        "~P": [
            ["he"], ["she"], ["it"], ["they"], ["me"], ["you"], ["mine"], ["yours"], ["theirs"]
        ],
        "~C": [
            ["and"], ["but"], ["or"], ["so"], ["as"], ["since"], ["if"], ["because"]
        ],
        "~I": [
            ["hey"], ["oops"], ["oh"], ["yeah"], ["yo"]
        ],
        "~J": [
            ["red"], ["green"], ["blue"], ["shiny"], ["short"], ["fast"]
        ],
        "~D": [
            ["very"], ["more"], ["even"], ["loudly"], ["cleanly"]
        ],
        "~R": [
            ["in"], ["on"], ["above"], ["below"], ["near"], ["far"]
        ],
        "~S": [

        ],
        "~E": [
            ["the"], ["a"], ["an"]
        ]
    }

    def generate(self, target="~SENTENCE"):
        """Randomly generate n grammatical sentences for the target."""
        if target in self.grammar:
            return self._generate(target).strip()
    
    
    def _generate(self, target):
        """Returns either the given target if it is a terminal symbol or a
        randomly generated string, possibly with a trailing space.
        """
        if target not in self.grammar:
            if target in punc_list:
                return target
            return " " + target

        if not self.grammar[target]:
            return "".join(self._generate(part) for part in choice(self.grammar_default[target]))
        return "".join(self._generate(part) for part in choice(self.grammar[target]))

    # Adds a structure to SENTENCE in the current grammar based on the passed message. The part of speech for
    # each word is taken from the dictionary based on the most common use of part of speech for each word.
    def addMessage(self, message, useStructure=True):
        message = message.replace('~', '')
        words = split(message)
        for i in range(len(words)):
            t = self.addWord(words[i])
            # Turns words from a message into a sentence structure
            if t in structure_types:
                words[i] = t
        if useStructure and any(("~" in w) for w in words): self.grammar["~SENTENCE"] += [words]

        
    def addWord(self, word):
        if word.lower() in self.dictionary:
            if not (word in self.dictionary):
                word = word.lower()
            if self.dictionary[word]:
                t = self.dictionary[word][0]
                self.grammar[t] += [[word]]
                return t
        

    def __init__(self, dict_file):
        with open(dict_file, "r") as file:
            for line in file.readlines():
                l = line.split()
                for i in range(1, len(l)):
                    l[i] = '~' + l[i]
                self.dictionary[l[0]] = l[1:]
        self.reset_grammar()
    
    def reset_grammar(self):
        self.grammar = copy.deepcopy(self.grammar_frame)

if __name__ == "__main__":
    g = generator("smalldictionary.txt")
    with open("test-data.txt", "r") as data:
        for line in data.readlines():
            g.addMessage(line)
    for _ in range(10):
        print(g.generate())
