


import random
from cafe import menu

class VikingHorde:

    _origin = random.choice(['Sweden', 'Norway', 'Denmark'])

    def pillage(self):
        if 'spam' in menu:
            print("this spam puts me in a pillaging mood")
        else:
            print("no it's too cold to pillage")


