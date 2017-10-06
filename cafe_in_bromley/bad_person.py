import sys

# person.py


#import good_cafe as cafe
import cafe

likes_spam = False

def order():
    if cafe.menu == ['spam']:
        print("I don't like spam")
    else:
        print("I'll have the baked beans")

