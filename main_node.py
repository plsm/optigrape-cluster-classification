import argparse
import collections
import csv
import datetime
import numpy.random
import os
import sklearn.neural_network
import time
import yaml

import command_line_arguments
import dataset

def main ():
    args = parse_arguments ()
    RNG = numpy.random.RandomState (args.RNG_seed)
    data_sets = dataset.load_data_sets (args.data_sets)
    parameters = load_neural_network_parameters (args.learning_parameters)
    suffix = filename_suffix (args)
    results_file, results_writer = open_results_file (suffix, parameters)
    NN_file, NN_writer = open_neural_network_file (suffix)
    for index in range (args.number_repeats):
        run_neural_network (RNG, args.fraction_test, data_sets, parameters, results_writer, NN_writer, index)
    results_file.close ()
    NN_file.close ()

def parse_arguments ():
    parser = argparse.ArgumentParser (
        description = "Optigrape worker"
    )
    command_line_arguments.data_sets_file (parser)
    command_line_arguments.fraction_test (parser)
    command_line_arguments.learning_parameters_file (parser)
    command_line_arguments.RNG_seed (parser)
    command_line_arguments.number_repeats (parser)
    return parser.parse_args ()

def load_neural_network_parameters (parameters_filename):
    with open (parameters_filename, "r") as fd:
        dictionary = yaml.load (fd)
        result = dictionary ["neural_network"]
        print ("Parameters of the neural network: {0}".format (result))
        return result

def run_neural_network (RNG, fraction_test, data_sets, parameters, results_writer, NN_writer, index_repeat):
    print ("I'm going to run neural network")
    train, test = dataset.split_data_sets_train_test (data_sets, fraction_test, RNG)
    clf = sklearn.neural_network.MLPClassifier (
        activation = parameters ["activation"],
        solver = parameters ["solver"],
        alpha = parameters ["alpha"],
        hidden_layer_sizes = parameters ["hidden_layers_size"],
        random_state = RNG,
        max_iter = parameters ["max_iterations"],
        early_stopping = parameters ["early_stopping"]
    )
    current_time = time.time ()
    clf.fit (train.xs, train.ys)
    ys = clf.predict (test.xs)
    score = compute_score (ys, test.ys)
    print ("Score is {0}".format (score))
    hit = random_chance_to_hit (train, test)
    write_results (results_writer, current_time, index_repeat, parameters, clf, score, hit)
    write_neural_network (NN_writer, current_time, index_repeat, clf)

def compute_score (classifier_ys, test_ys):
    score = 0
    for an_y, a_test_y in zip (classifier_ys, test_ys):
        if all ([ay == at for ay, at in zip (an_y, a_test_y)]):
            score += 1
    return score / float (len (test_ys))

def random_chance_to_hit (train, test):
    # type: (dataset.Function, dataset.Function) -> float
    """
    Compute the chance of a random classifier to correctly classify a sample in the test set, given a training set.
    :param test:
    :type train: dataset.Function
    :type test: dataset.Function
    """
    def compute_classes_occurrence (l):
        # type: (collections.Iterable) -> dict
        r = {}
        for x in l:
            if x in r:
                r [x] = r [x] + 1
            else:
                r [x] = 1
        return r
    count_classes_train = compute_classes_occurrence (train.IDs)
    count_classes_test = compute_classes_occurrence (test.IDs)
    result = sum ([count_classes_train [key] * count_classes_test [key] for key in count_classes_test.keys ()])
    result = result / float (len (train.IDs) * len (test.IDs))
    return result

def filename_suffix (args):
    # type: (argparse.Namespace) -> str
    data = datetime.datetime.now ().__str__().split ('.') [0]
    data = data.replace (' ', '-').replace (':', '-')
    result = "results_{0}_{1}_{2}_{3}_{4}_{5}.csv".format (
        os.path.basename (args.data_sets),
        os.path.basename (args.learning_parameters),
        args.RNG_seed,
        os.getenv ("SGE_TASK_ID"),
        os.getenv ("JOB_ID"),
        data
    )
    return result

def open_results_file (suffix, parameters):
    # type: (str, dict) -> object
    results_file = open ("results_{0}.csv".format (suffix), "w")
    results_writer = csv.writer (results_file, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
    header_row = [
        "time",
        "run",
        "activation",
        'solver',
        "alpha",
        'early.activation',
        'max.iterations'
    ] + [
        'hidden.layer.{0:d}.size'.format (index + 1) for index in range (len (parameters ["hidden_layers_size"]))
    ] + [
        "num.iterations",
        "score",
        "random.chance.win"
    ]
    results_writer.writerow (header_row)
    return results_file, results_writer

def open_neural_network_file (suffix):
    NN_file = open ("neural-network_{0}.csv".format (suffix), "w")
    NN_writer = csv.writer (NN_file, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
    return NN_file, NN_writer

def write_results (results_writer, current_time, index_repeat, parameters, clf, score, hit):
    row = [
        current_time,
        index_repeat,
        parameters ["activation"],
        parameters ["solver"],
        parameters ["alpha"],
        parameters ["early_stopping"],
        parameters ["max_iterations"]
    ] + parameters ["hidden_layers_size"] + [
        clf.n_iter_,
        score,
        hit
    ]
    results_writer.writerow (row)

def write_neural_network (NN_writer, current_time, index_repeat, clf):
    row = [current_time, index_repeat, clf.out_activation_, clf.n_layers_, clf.n_outputs_]
    for matrix in clf.coefs_:
        for cr in matrix:
            row.extend (cr)
    for r in clf.intercepts_:
        row.extend (r)
    NN_writer.writerow (row)


if __name__ == "__main__":
    main ()
