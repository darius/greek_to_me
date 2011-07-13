"""
Test a language-guesser module against labeled test data.
Sample usage:
$ python punditeval.py models

The input's in a file named test-data (not supplied, sorry).
Input lines look like
  en I am a blah blah blah
  es Yo hablo un poco blabla
  UNKNOWN UOEAAA$#@$%$#""%@

Output lines look like
X  0.6 -123 de:-25.9 ... kr:-47.0 en I am a blah blah blah
   2.8 -100 es:-23.0 ... kr:-47.5 es Yo hablo un poco blabla
where the first line shows a wrong guess.
"""

import math

import greek_to_me

def main(argv):
    "Try the given pundit on the test-data file."
    p = greek_to_me.make_pundit(argv[1])
    print p.get_id()
    evaluate(p, open('test-data'))

def evaluate(p, file):
    "Print results from the pundit p applied to the inputs from file."
    results = [foo(p, line.rstrip('\n').split(' ', 1)) for line in file]
    for diffstr, pc, ok, results, language, text in sorted(results):
        resultstr = ' '.join('%s:%05.1f' % (language, score)
                             for score, language in results)
        print ok, diffstr, pc, resultstr, language, text

def foo(p, (language, text)):
    """Apply pundit p to the given text, which is supposedly in the
    given language. Return stats."""
    diff, ok, results, language, text = classify(p, (language, text))
    perchar = results[0][0] / float(len(text))
    return '%4.1f' % diff, int(perchar * 100), ok, results, language, text

def classify(p, (language, text)):
    """Apply pundit p to the given text, checking if it judges the
    given language the most probable."""
    results = p.judge(text)
    guessed = results[0][1]
    ok = ' ' if guessed == language else 'X'
    diff = results[0][0] - results[1][0]
    return diff, ok, results, language, text


if __name__ == '__main__':
    import sys
    main(sys.argv)
