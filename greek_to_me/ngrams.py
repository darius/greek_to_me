"""
Letter n-gram language model.
"""

import cPickle
from collections import defaultdict
import hashlib
from math import log10

def get_source_code_version_id():
    return '$Rev'

class NGramModel:

    def __init__(self, filename=None, order=None, training_lines=None):
        if filename:
            self.load(filename)
        else:
            self.train(order, training_lines)

    def train(self, order, training_lines):
        self.order = order
        self.get_ngrams = ngram_splitter(order)
        self.counts = defaultdict(IntDictMaker())
        for prefix, char in training(training_lines, self.get_ngrams):
            self.counts[prefix][char] += 1
        self._update_totals()

    def load(self, filename):
        self.order, self.counts = cPickle.load(open(filename, 'rb'))
        self.get_ngrams = ngram_splitter(self.order)
        self._update_totals()

    def save(self, filename):
        cPickle.dump((self.order, self.counts), open(filename, 'wb'))

    def get_id(self):
        "Return a code identifying the data we trained on."
        s = str(self.order) + ','
        for prefix in sorted(self.counts):
            for char, count in sorted(self.counts[prefix].items()):
                s += char + str(count) + ','
        return hex_encode(hash(s.encode('utf8')))

    def score(self, text):
        """Return the log10 of the conditional probability of the text,
        given the text's length, according to our model."""
        return sum(self.log_probability(prefix, char)
                   for prefix, char in self.get_ngrams(text))

    def log_probability(self, prefix, char):
        return log10(self.probability(prefix, char))

    def probability(self, prefix, char):
        # n + 1/2 smoothing
        return (self.counts[prefix].get(char, 0) + 0.5) / self.totals[prefix]

    def _update_totals(self):
        default_total = 0.5 * len(alphabet)
        self.totals = defaultdict(lambda: default_total)
        for prefix in self.counts:
            self.totals[prefix] = (sum(self.counts[prefix].values())
                                   + default_total)

class IntDictMaker:
    "Like lambda: defaultdict(int), but picklable."
    def __call__(self):
        return defaultdict(int)


# To help make these judgements reproducible:

hasher = hashlib.md5()

def hash(bytes):
    h = hasher.copy()
    h.update(bytes)
    return h.digest()

def hex_encode(bytes):
    def _enc(c):
        assert ord(c) <= 0xFF
        return hex(ord(c))[2:]
    return ''.join(map(_enc, bytes))


# Process inputs in some standard ways:

def training(lines, get_ngrams):
    for line in lines:
        text = line.rstrip('\n')
        for prefix, char in get_ngrams(text):
            yield prefix, char

def ngram_splitter(order):
    if order == 2: return bigrams
    if order == 3: return trigrams
    assert False

def bigrams(text):
    w = ''.join(normalize(text))
    return ((p, r) for p, r in zip(' '+w, w+' '))

def trigrams(text):
    w = ''.join(normalize(text))
    return ((p+q, r) for p, q, r in zip('  '+w, ' '+w+' ', w+'  '))

import string
selfeval = set(" '" + string.ascii_lowercase)
alphabet = '.' + ''.join(selfeval)

def normalize(text):
    return ((c if c in selfeval else '.') for c in text)
