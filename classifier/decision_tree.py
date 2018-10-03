import csv
import sklearn.tree
import yaml

import base_algorithm
import dataset

class Decision_Tree (base_algorithm.Base_Algorithm):
    def __init__ (self):
        base_algorithm.Base_Algorithm.__init__ (self)

    def load_parameters (self, filename):
        with open (filename, "r") as fd:
            dictionary = yaml.load (fd)
            result = dictionary ["decision_tree"]
            print ("Parameters of the decision tree: {0}".format (result))
            return result

    def open_results_file (self):
        # type: () -> (object, object)
        results_file = open ("decision-tree_results_{0}.csv".format (self.suffix), "w")
        results_writer = csv.writer (results_file, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
        header_row = [
            "time",
            "run",
            "criterion",
            'max.depth',
            "min.samples.split",
            "score",
            "random.chance.win"
        ]
        results_writer.writerow (header_row)
        return results_file, results_writer

    def open_classifier_file (self):
        classifier_file = open ("decision-tree_structure_{0}.csv".format (self.suffix), "w")
        classifier_writer = csv.writer (classifier_file, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
        return classifier_file, classifier_writer

    def run (self, fraction_test, index_repeat):
        print ("I'm going to run decision tree")
        train, test = dataset.split_data_sets_train_test (self.data_sets, fraction_test, self.RNG)
        clf = sklearn.tree.DecisionTreeClassifier (
            criterion = self.parameters ["criterion"],
            max_depth = self.parameters ["max_depth"],
            min_samples_split = self.parameters ["min_samples_split"],
            random_state = self.RNG
        )
        current_time, score, hit = self.run_classifier (clf, train, test)
        self.write_decision_tree_results (current_time, index_repeat, score, hit)
        self.write_decision_tree_structure (current_time, index_repeat, clf)

    def write_decision_tree_results (self, current_time, index_repeat, score, hit):
        row = [
            current_time,
            index_repeat,
            self.parameters ["criterion"],
            self.parameters ["max_depth"],
            self.parameters ["min_samples_split"],
            score,
            hit
        ]
        self.results_writer.writerow (row)

    def write_decision_tree_structure (self, current_time, index_repeat, classifier):
        row = [
            current_time,
            index_repeat,
            classifier.tree_.node_count
        ] + [x for x in classifier.tree_.children_left] + \
              [x for x in classifier.tree_.children_right] + \
              [x for x in classifier.tree_.feature] + \
              [x for x in classifier.tree_.threshold]
        self.classifier_writer.writerow (row)

if __name__ == '__main__':
    Decision_Tree ()
