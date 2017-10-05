import sys

def eat():
    print("Ate {} in {}".format(__name__, __package__))
    print(sys.modules[__name__])
    return "Ate {}".format(__name__)