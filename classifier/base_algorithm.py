import argparse
import collections
import datetime
import numpy
import os.path
import time

import command_line_arguments
import dataset

class Base_Algorithm:
    """
    Contains functions used by all classifier algorithms.
    Derived classes should implement the methods load_parameters, open_results_file, open_classifier_file and run.
    """
    def __init__(self):
        """
        Instantiate a classifier using command line options and run it.
        """
        args = parse_arguments ()
        self.RNG = numpy.random.RandomState (args.RNG_seed)
        self.data_sets = dataset.load_data_sets (args.data_sets)
        self.parameters = self.load_parameters (args.learning_parameters)
        self.suffix = self.__filename_suffix (args)
        results_file, self.results_writer = self.open_results_file ()
        classifier_file, self.classifier_writer = self.open_classifier_file ()
        output_file, self._output_writer = self.open_output_file ()
        for index in range (args.number_repeats):
            self.run (args.fraction_test, index)
        results_file.close ()
        classifier_file.close ()
        output_file.close ()

    @staticmethod
    def __filename_suffix (args):
        # type: (argparse.Namespace) -> str
        """
        Compute a filename suffix used in the file with the classification task results and in the file with the classifier data.
        :param args:
        :return:
        """
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
        Runs the given classifier on the given training set and evaluate it on the test set.
        The classifier should provide a fit and predict methods
        :param classifier: One of the classifiers defined in the sklearn package.
        :param train: the training set.
        :param test: the test set.
        :return: a tuple with current time, classification score and the probability of randomly guessing the correct class.
        """
        current_time = time.time ()
        classifier.fit (train.xs, train.ys)
        ys = classifier.predict (test.xs)
        self._write_classifier_output (ys, test.ys)
        score = self.compute_score (ys, test.ys)
        print ("Score is {0}".format (score))
        hit = self.random_chance_to_hit (train, test)
        return current_time, score, hit

    @staticmethod
    def compute_score (classifier_ys, test_ys):
        """
        Compute the classification score, meaning the fraction of correctly classified records.
        The arguments are either a list of integers or a list of list of objects.
        The first case is the output of uni-dimensional classifiers, while the second case is the output of multi-dimensional classifiers.
        :param classifier_ys: The classifier output.
        :param test_ys: The correct class.
        :return: A floating point number representing the classification score.
        """
        all_score = 0
        partial_count = {}
        if isinstance (classifier_ys [0], numpy.ndarray) and isinstance (test_ys [0], list):
            for an_y, a_test_y in zip (classifier_ys, test_ys):
                key = tuple (a_test_y)
                if key not in partial_count:
                    partial_count [key] = [0, 0]
                if all ([ay == at for ay, at in zip (an_y, a_test_y)]):
                    all_score += 1
                    partial_count [key][0] += 1
                partial_count [key][1] += 1
        elif isinstance (classifier_ys [0], int) and isinstance (test_ys [0], int):
            for an_y, a_test_y in zip (classifier_ys, test_ys):
                key = a_test_y
                if key not in partial_count:
                    partial_count [key] = [0, 0]
                if an_y == a_test_y:
                    all_score += 1
                    partial_count [key] [0] += 1
                partial_count [key] [1] += 1
        else:
            print '{}'.format (type (classifier_ys [0]))
            print '{}'.format (type (test_ys [0]))
            raise Exception ('[E] Unknown class type of {} {}'.format (classifier_ys, test_ys))
        classes = partial_count.keys ()
        classes.sort ()
        partial_score = [
            partial_count [key][0] / float (partial_count [key][1])
            for key in classes
        ]
        all_score = all_score / float (len (test_ys))
        result = [all_score] + partial_score
        return result

    def _write_classifier_output (self, classifier_ys, test_ys):
        if isinstance (classifier_ys [0], numpy.ndarray) and isinstance (test_ys [0], list):
            for an_y, a_test_y in zip (classifier_ys, test_ys):
                row = list (an_y) + a_test_y
                self._output_writer.writerow (row)
        elif isinstance (classifier_ys [0], int) and isinstance (test_ys [0], int):
            for an_y, a_test_y in zip (classifier_ys, test_ys):
                row = [an_y, a_test_y]
                self._output_writer.writerow (row)
        else:
            print '{}'.format (type (classifier_ys [0]))
            print '{}'.format (type (test_ys [0]))
            raise Exception ('[E] Unknown class type of {} {}'.format (classifier_ys, test_ys))

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

    def open_output_file (self):
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
