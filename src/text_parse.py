from nltk.parse.stanford import StanfordDependencyParser
from config import config
from nltk.corpus import  wordnet
from random import choice
import inflect

dependency_parser = StanfordDependencyParser(path_to_jar=config['JAVA']['stanford-parser'].strip(), path_to_models_jar=config['JAVA']['stanford-parser-models'].strip())

class langParse():
    def __init__(self, sentence):
        self.dep_tree = []
        self.sentence = sentence
        self.types = {
            # More here: http://demo.ark.cs.cmu.edu/parse/about.html
            "NN" : [], # Common singular noun
            "NNS": [], # Common plural
            "PRP": [], # Personal pronoun
            "VB" : [], # Past tense verb
            "VBP" : [], # Present tense verb
            "VBD" : [], # Past tense verb
            "VBG" : [], # -ing verb
            "JJ" : [], # Adjective
            "RB" : [], # Adverb
        }
        self.syns = {}
        self.dep_tree = self.create_dep_tree(self.sentence)
        self.assign_words()
        self.nouns = [x.name().split('.', 1)[0] for x in wordnet.all_synsets('n')]
        self.verbs = [x.name().split('.', 1)[0] for x in wordnet.all_synsets('v')]

    def create_dep_tree(self,text):
        result = dependency_parser.raw_parse(text)
        dep = result.__next__()
        return list(dep.triples())

    def assign_words(self):
        for i in self.dep_tree:
            for j in i:
                try:
                    if j[0] not in self.types[j[1]]:
                        self.types[j[1]].append(j[0])
                except KeyError:
                    continue
        print(self.types)

    @staticmethod
    def find_syns(syn_word_lst, word_type="", similar_tos=False, lim=99):
        words = []
        for syn_word in syn_word_lst:
            for meaning,ss in enumerate(wordnet.synsets(syn_word,word_type)):
                if word_type == "n" and meaning == lim:
                    break
                elif word_type == "v" and meaning == lim:
                    break
                print(ss.name(), ss.lemma_names(),meaning)
                words.append(ss.lemma_names())
                if similar_tos:
                    for sim in ss.similar_tos():
                        words.append(sim.lemma_names())
        words = [item.replace("_"," ") for sublist in words for item in sublist]
        print(words)
        return words


def form_phrase(intro, text, end,extras, check_words=True, capitalized=False, must_have_verb_and_noun=True):
    langp = langParse(text)
    pluralizer = inflect.engine()
    # Get a list of all verbs
    verbs = langp.types["VBP"] + langp.types["VB"] + langp.types["VBD"]
    if not verbs:
        return
    # Get a list of all nouns
    present_nouns = langp.types["NNS"] + langp.types["NN"]
    # Get a list of all adverbs
    adverbs = langp.types["RB"]
    # Get a list of all adjectives
    adjectives = langp.types["JJ"]
    # Get a list of synonyms of the verbs/nouns
    v_syns = langp.find_syns(verbs,"v",extras)
    n_syns = langp.find_syns(present_nouns,"n",extras)
    if check_words: # Verify the found words are valid
        v_syns = [i for i in v_syns if i in langp.verbs]
        n_syns = [i for i in n_syns if i in langp.nouns]
    # Make the noun synonyms plural
    n_syns = [pluralizer.plural(i) for i in n_syns]
    if not must_have_verb_and_noun or (not v_syns or not n_syns):
        return
    result_phrase = (choice(intro) if intro else "") + (" " + choice(adverbs) if adverbs else "") + (" " + choice(v_syns) if v_syns else "") + (" " + (choice(adjectives) + " " if adjectives else "") + "#" + choice(n_syns) if n_syns else "") + choice(end)
    if capitalized:
        result_phrase = result_phrase.upper()
    return result_phrase
