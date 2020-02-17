import random
import numpy as np

def parse_line(line):
    line = line.split("\t")
    return line[0], line[1], int(line[2] == "OFF")

def read_file(_set):
    with open("OffensEval/offenseval-" + _set + "-training-v1.tsv") as fi:
        lines = fi.read().splitlines()
        ids, x_train, y_train = zip(*list(map(lambda x: parse_line(x), lines[1:])))

    return [ {"id":i, "text":x, "label": y} for i, x, y in zip(ids, x_train, y_train) ]

def fold_iterator(all_samples, K=10, dev_ratio=0.10, random_seed=1234):
    """yields K tuples of shape (train, dev, test) """
    random.seed(random_seed)
    random.shuffle(all_samples) # initial shuffle
    _all = np.array(all_samples) # convert to numpy for list indexing

    fold_size = len(all_samples) // K
    dev_size = int(len(all_samples) * dev_ratio)
    indices = set([x for x in range(len(all_samples))])

    for i in range(0, K):
        test = set([ x for x in range(fold_size * i, fold_size * (i+1)) ])
        rest = list(indices.difference(test))   # get indices of the rest samples
        random.shuffle(rest)    # shuffle before splitting into train and dev
        yield (_all[rest[dev_size:]], _all[rest[:dev_size]], _all[list(test)])
    return