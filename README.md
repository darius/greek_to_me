This Python module takes text input and guesses what natural language
it's in:

    >>> from greek_to_me import make_pundit
    >>> p = make_pundit('models')   # The models/ dir in this distro
    >>> p.best_guess('hello world')
    'en'   # English
    >>> p.best_guess('hola mundo')
    'es'   # Espanol

You can also build new models and ask the pundit for more info if you
want a measure of confidence or want to make more subtle
discriminations, e.g. to combine this textual evidence with an
Accept-Language header.

See the code for docs. smoketest.py shows some sample usage.

The judgments use a character n-gram model of each language. Supplied
with this module in `models/` are some bigram models built from the
Europarl and Leipzig parallel corpora, mostly for European languages.
(In code not supplied here, I first used
http://pypi.python.org/pypi/guess-language to screen out text in other
languages like Mandarin. So why not use guess-language for the whole
job? Because it works poorly on very short inputs like search queries;
our approach needs less evidence to reach a reasonable judgement.)

IIRC trigram models do noticeably better but take an order of
magnitude more space; I didn't feel like checking 4MB into this repo.

See http://alias-i.com/lingpipe/demos/tutorial/langid/read-me.html
for a similar but more sophisticated package in Java.
