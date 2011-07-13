import greek_to_me

pundit = greek_to_me.make_pundit('models')

def print_judgement(text):
    "Print the top 2 languages for 'text', and their scores."
    judgments = pundit.judge(text)
    print text
    print judgments[:2]
    print

print_judgement('Hello, world!')
print_judgement('Hello, world! How are you?')
print_judgement('Hola a el mundo.')

print 'Candidates:', ' '.join(sorted(pundit.get_candidates()))

priors = dict(en=0.6, es=0.2, nl=0.1, it=0.1)

print pundit.best_guess('Hello, world!')
print pundit.best_guess('Hello, world!', priors)

print pundit.best_guess('Hola mundo')
print pundit.best_guess('Hola mundo', priors)
