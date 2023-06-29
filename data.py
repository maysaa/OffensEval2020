import random
import numpy as np
from sklearn.model_selection import StratifiedKFold, train_test_split

def parse_line(line):
    line = line.split("\t")
    return line[0], line[1], int(line[2] == "OFF")

def read_file(_set):
    # with open("OffensEval/"+ _set +".tsv", "r", encoding="utf-8") as fi:
    with open("AFND_Dataset/"+ _set +".tsv", "r", encoding="utf-8") as fi:
        lines = fi.read().splitlines()
        ids, x_train, y_train = zip(*list(map(lambda x: parse_line(x), lines[1:])))

    return [ {"id":i, "text":x, "label": y} for i, x, y in zip(ids, x_train, y_train) ]

def fold_iterator_sklearn(all_samples, K=10, dev_ratio=0.10, random_seed=1234):
    """yields K tuples of shape (train, dev, test) """
    random.seed(random_seed)
    random.shuffle(all_samples) # initial shuffle
    _all = np.array(all_samples) # convert to numpy for list indexing

    skf = StratifiedKFold(n_splits=K)
    skf.get_n_splits(_all, [ y["label"] for y in _all])

    for train_index, test_index in skf.split(_all, [ y["label"] for y in _all]):
        trn, dev = train_test_split(_all[train_index], test_size=dev_ratio, random_state=random_seed)
        yield (trn, dev, _all[test_index])
    return

