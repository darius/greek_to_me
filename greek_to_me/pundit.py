"""
A discriminator running a set of language models over the same text.
"""

import os

import ngrams
from ngrams import NGramModel

def get_source_code_version_id():
    return '$Rev'


def make_pundit(dirname, language_codes=None):
    if language_codes is None:
        language_codes = \
            [lc
             for lc, ext in map(os.path.splitext, os.listdir(dirname))
             if ext == '.model']
    def j(filename):
        return os.path.join(dirname, filename)
    return LanguagePundit([(lc, NGramModel(j('%s.model' % lc)))
                           for lc in language_codes])

class LanguagePundit:

    def __init__(self, models):
        self.models = dict(models)

    def get_id(self):
        """Return a reasonably-compact code identifying both the
        source code and the data that together produce our judgments."""
        return (get_source_code_version_id(),
                ngrams.get_source_code_version_id(),
                [(lc, model.get_id())
                 for lc, model in sorted(self.models.items())])

    def get_candidates(self):
        "Return a list of the language codes we know about."
        return self.models.keys()

    def best_guess(self, text, priors=None):
        "Return the language code of the most likely language of 'text'."
        candidates = (self.judge(text) if priors is None 
                      else self.posteriors(text, priors))
        score, lc = candidates[0]
        return lc

    def judge(self, text):
        """Return the log10-probability each model assigns to the
        text, with highest first."""
        return sorted(((model.score(text), lc)
                       for lc, model in self.models.iteritems()),
                      reverse=True)

    def posteriors(self, text, priors):
        """Given a dict from language code to prior probability,
        return a list of (p, lc): the probability of each language
        given the text, and its language code (in descending order
        of probability)."""
        # Get each model's value for the probability of the text:
        ps = [(lc, priors.get(lc, 0) * 10**model.score(text))
              for lc, model in self.models.items()]
        total = float(sum(p for lc, p in ps))
        # The probability of each language, given the text, then, is:
        return sorted(((p / total, lc) for lc, p in ps),
                      reverse=True)
