import random
import os


MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
ASSETS_DIR = os.path.join(MAIN_DIR, "asset")


# helper function to help with ranges of values to randomly
# choose from (or do nothing if it's a value)
def resolve_range(t):
    if hasattr(t, "__getitem__"):
        if len(t) != 2:
            raise ValueError("Range %s contains more than 2 values" % str(t))
        if t[0] > t[1]:
            t = (t[1], t[0])
        if type(t[0]) is int:
            return random.randint(*t)
        elif type(t[0]) is float:
            lower = min(t)
            upper = max(t)
            return random.random() * (upper - lower) + lower
    # a scalar
    return t
