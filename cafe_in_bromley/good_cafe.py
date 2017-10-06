import sys


# cafe.py
import person
print(sys.modules['person'].__dict__.keys())

if person.likes_spam:
    menu = ['eggs', 'baked beans']
else:
    menu = ['spam']


