import csv
import sklearn.neural_network
import yaml

import base_algorithm
import dataset

class Neural_Network (base_algorithm.Base_Algorithm):
    def __init__ (self):
        base_algorithm.Base_Algorithm.__init__ (self)

    def load_parameters (self, filename):
        with open (filename, "r") as fd:
            dictionary = yaml.load (fd)
            result = dictionary ["neural_network"]
            print ("Parameters of the neural network: {0}".format (result))
            return result

    def open_results_file (self):
        results_file = open ("neural-network_results_{0}.csv".format (self.suffix), "w")
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
            'hidden.layer.{0:d}.size'.format (index + 1) for index in range (len (self.parameters ["hidden_layers_size"]))
        ] + [
            "num.iterations",
            "all.score",
        ] + ["partial.score.{}".format (index) for index in range (dataset.DataSet.CLASS_COUNTER)] + [
            "random.chance.win"
        ]
        results_writer.writerow (header_row)
        return results_file, results_writer

    def open_classifier_file (self):
        NN_file = open ("neural-network_classifier_{0}.csv".format (self.suffix), "w")
        NN_writer = csv.writer (NN_file, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
        return NN_file, NN_writer

    def open_output_file (self):
        filename = 'neural-network_output_{0}.csv'.format (self.suffix)
        output_file = open (filename, 'w')
        output_writer = csv.writer (output_file, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
        header_row = [
            'predicted.class.{}'.format (index + 1)
            for index in range (dataset.DataSet.CLASS_COUNTER)
        ] + [
            'real.class.{}'.format (index + 1)
            for index in range (dataset.DataSet.CLASS_COUNTER)
        ] + [
            'run'
        ]
        output_writer.writerow (header_row)
        return output_file, output_writer

    def run (self, fraction_test, index_repeat):
        print ("I'm going to run neural network")
        train, test = dataset.split_data_sets_train_test (self.data_sets, fraction_test, self.RNG)
        clf = sklearn.neural_network.MLPClassifier (
            activation = self.parameters ["activation"],
            solver = self.parameters ["solver"],
            alpha = self.parameters ["alpha"],
            hidden_layer_sizes = self.parameters ["hidden_layers_size"],
            random_state = self.RNG,
            max_iter = self.parameters ["max_iterations"],
            early_stopping = self.parameters ["early_stopping"]
            )
        current_time, score, hit = self.run_classifier (clf, train, test, index_repeat)
        self.write_neural_network_results (current_time, index_repeat, clf, score, hit)
        self.write_neural_network_sructure (current_time, index_repeat, clf)

    def write_neural_network_results (self, current_time, index_repeat, clf, score, hit):
        row = [
            current_time,
            index_repeat,
            self.parameters ["activation"],
            self.parameters ["solver"],
            self.parameters ["alpha"],
            self.parameters ["early_stopping"],
            self.parameters ["max_iterations"]
        ] + self.parameters ["hidden_layers_size"] + [
            clf.n_iter_,
        ] + score + [
            hit
        ]
        self.results_writer.writerow (row)

    def write_neural_network_sructure (self, current_time, index_repeat, clf):
        row = [current_time, index_repeat, clf.out_activation_, clf.n_layers_, clf.n_outputs_]
        for matrix in clf.coefs_:
            for cr in matrix:
                row.extend (cr)
        for r in clf.intercepts_:
            row.extend (r)
        self.classifier_writer.writerow (row)

if __name__ == '__main__':
    Neural_Network ()
