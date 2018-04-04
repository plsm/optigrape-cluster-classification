import csv

import rng

class DataSet:
    CLASS_COUNTER = 1

    def __init__ (self, filename):
        print ("Reading CSV file {0}...".format (filename))
        self.filename = filename
        with open (filename, "r") as fd:
            reader = csv.reader (fd, delimiter = '\t', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
            reader.next ()
            self.rows = [row for row in reader]
        self.class_id = DataSet.CLASS_COUNTER
        DataSet.CLASS_COUNTER += 1

    def split_two_sets (self, fraction_second):
        """
        Randomly divide the data set into two sets. We make sure that both sets have at least one element.
        :param fraction_second: probability that an element is added to the second set.
        :return: A pair of lists
        """
        result = {0: [], 1:[]}
        for element in self.rows [1:]:
            index = 1 if rng.flip_coin (fraction_second) else 0
            result [index].append (element)
        if len (result [0]) == 0:
            index = 0
            result [0].append (self.rows [0])
        elif len (result [1]) == 0:
            index = 1
        else:
            index = 1 if rng.flip_coin (fraction_second) else 0
        result [index].append (self.rows [0])
        return result [0], result [1]

    def __str__ (self):
        def add (result, rs):
            for r in rs:
                if shorten_horizontally:
                    result += "{0}, ... {1}\n".format (str (r [:idx1])[:-1], str (r [idx2:])[1:])
            return result
        result = "Data set in file {0}\nClass {1}\n".format (self.filename, self.class_id)
        shorten_horizontally = len (self.rows [0]) > 12
        if shorten_horizontally:
            idx1 = 5
            idx2 = len (self.rows [0]) - 5
        if len (self.rows) > 12:
            result = add (result, self.rows [:5])
            result += "...\n"
            result = add (result, self.rows [-5:])
        else:
            result = add (result, self.rows)
        return result

class Function:
    def __init__ (self):
        self.xs = []
        self.ys = []

    def __str__ (self):
        result = ""
        for x, y in zip (self.xs, self.ys):
            result += y + " = " + y + "\n"
        return result

def split_data_sets_train_test (list_data_sets, fraction_test):
    """

    :param list_data_sets:
    :param fraction_test:
    :return:
    """
    xs_splits = [d.split_two_sets (fraction_test) for d in list_data_sets]
    ys_splits = [(len (xs [0]) * [d.class_id], len (xs [1]) * [d.class_id]) for xs, d in zip (xs_splits, list_data_sets)]
    result = {0: Function (), 1: Function ()}
    for xs, ys in zip (xs_splits, ys_splits):
        for index in range (2):
            result [index].xs.extend (xs [index])
            result [index].ys.extend (ys [index])
    return result [0], result [1]
