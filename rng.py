import random

INITIAL_STATE = None

def init (args):
    global INITIAL_STATE
    random.seed (args.RNG_seed)
    INITIAL_STATE = random.getstate ()

def next_index (range):
    """
    Return an index, i.e. a number between 0 and range-1.
    This is useful to select an element from a sequence.
    :param range: The index range
    :return: a random index.
    """
    return random.randint (0, range - 1)

def flip_coin (true_probability):
    return random.random () < true_probability
