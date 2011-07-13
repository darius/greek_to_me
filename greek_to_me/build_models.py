#!/usr/bin/env python
"""
Build models from our standard corpora.

Usage: 
  $ rm -r bigram_models trigram_models
  $ ./build_models.py bigram_models 2
  $ ./build_models.py trigram_models 3
"""

import os

from ngrams import NGramModel

def main(argv):
    outdir = argv[1]
    order = int(argv[2])
    indir = 'parallel-corpora/smallish-texts/'

    os.mkdir(outdir)
    def outfile(lc):
        return os.path.join(outdir, lc + '.model')

    for lc in os.listdir(indir):
        infile = os.path.join(indir, lc)
        make_model_from_corpus(infile, order).save(outfile(lc))
 
def make_model_from_corpus(filename, order):
    print 'Training on %s...' % filename
    return NGramModel(order=order, training_lines=open(filename))


if __name__ == '__main__':
    import sys
    main(sys.argv)
