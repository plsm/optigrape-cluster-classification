import argparse
import collections
import datetime
import numpy
import os.path
import time

import command_line_arguments
import dataset

class Base_Algorithm:
    def __init__(self):
        args = parse_arguments ()
        self.RNG = numpy.random.RandomState (args.RNG_seed)
        self.data_sets = dataset.load_data_sets (args.data_sets)
        self.parameters = self.load_parameters (args.learning_parameters)
        self.suffix = self.__filename_suffix (args)
        results_file, self.results_writer = self.open_results_file ()
        classifier_file, self.classifier_writer = self.open_classifier_file ()
        for index in range (args.number_repeats):
            self.run (args.fraction_test, index)
        results_file.close ()
        classifier_file.close ()

    @staticmethod
    def __filename_suffix (args):
        # type: (argparse.Namespace) -> str
        data = datetime.datetime.now ().__str__ ().split ('.') [0]
        data = data.replace (' ', '-').replace (':', '-')
        result = "{0}_{1}_{2}_{3}_{4}_{5}_{6}".format (
            os.path.basename (args.data_sets),
            os.path.basename (args.learning_parameters),
            args.RNG_seed,
            args.fraction_test,
            os.getenv ("SGE_TASK_ID"),
            os.getenv ("JOB_ID"),
            data
        )
        return result

    def run_classifier (self, classifier, train, test):
        """

        :param classifier:
        :param train:
        :param test:
        :return:
        """
        current_time = time.time ()
        classifier.fit (train.xs, train.ys)
        ys = classifier.predict (test.xs)
        score = self.compute_score (ys, test.ys)
        print ("Score is {0}".format (score))
        hit = self.random_chance_to_hit (train, test)
        return current_time, score, hit

    @staticmethod
    def compute_score (classifier_ys, test_ys):
        score = 0
        for an_y, a_test_y in zip (classifier_ys, test_ys):
            if all ([ay == at for ay, at in zip (an_y, a_test_y)]):
                score += 1
        return score / float (len (test_ys))

    @staticmethod
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

    def load_parameters (self, filename):
        raise Exception ('Not overloaded')

    def open_results_file (self):
        raise Exception ('Not overloaded')

    def open_classifier_file (self):
        raise Exception ('Not overloaded')

    def run (self, fraction_test, index):
        raise Exception ('Not overloaded')

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
