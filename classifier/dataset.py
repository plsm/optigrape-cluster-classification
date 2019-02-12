import csv
import yaml

class DataSet:
    CLASS_COUNTER = 0

    def __init__ (self, filename, class_name, has_header):
        print ("Reading CSV file {0}...".format (filename))
        self.filename = filename
        with open (filename, "r") as fd:
            reader = csv.reader (fd, delimiter = '\t', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
            if has_header:
                reader.next ()
            self.rows = [row for row in reader]
        self.class_name = class_name
        DataSet.CLASS_COUNTER += 1
        self.class_ID = DataSet.CLASS_COUNTER

    def split_two_sets (self, fraction_second, RNG):
        """
        Randomly divide the data set into two sets. We make sure that both sets have at least one element.
        :type fraction_second: float
        :type RNG: numpy.random.RandomState
        :param RNG:
        :param fraction_second: probability that an element is added to the second set.
        :return: A pair of non-empty lists
        """
        result = {0: [], 1:[]}
        for element in self.rows [1:]:
            index = RNG.binomial (1, fraction_second)
            result [index].append (element)
        if len (result [0]) == 0:
            index = 0
        elif len (result [1]) == 0:
            index = 1
        else:
            index = RNG.binomial (1, fraction_second)
        result [index].append (self.rows [0])
        return result [0], result [1]

    def __str__ (self):
        def add (result, rs, first = False):
            for r in rs:
                if shorten_horizontally:
                    result += "{0}, {2} {1}\n".format (
                        str (r [:idx1])[:-1],
                        str (r [idx2:])[1:],
                        "... {0} columns ...".format (len (self.rows [0]) - 10) if first else "..."
                    )
                else:
                    result += "{0}\n".format (r)
                first = False
            return result
        result = "Data set in file {0}\nClass {1}\n".format (self.filename, self.class_name)
        shorten_horizontally = len (self.rows [0]) > 12
        if shorten_horizontally:
            idx1 = 5
            idx2 = len (self.rows [0]) - 5
        if len (self.rows) > 12:
            result = add (result, self.rows [:5], True)
            result += "... {0} rows ...\n".format (len (self.rows) - 10)
            result = add (result, self.rows [-5:])
        else:
            result = add (result, self.rows)
        return result

class Function:
    def __init__ (self):
        self.xs = []
        self.ys = []
        self.IDs = []

    def __str__ (self):
        def add (result, x, y, first = False):
            result += "{0} = ".format (y)
            if shorten_horizontally:
                result += "{0}, {2} {1}\n".format (
                    str (x [:idx1]) [:-1],
                    str (x [idx2:]) [1:],
                    "... {0} columns ...".format (len (x) - 10) if first else "..."
                )
            else:
                result += "{0}\n".format (x)
            return result
        result = ""
        xsys = zip (self.xs, self.ys)
        shorten_horizontally = len (xsys [0][0]) > 12
        if shorten_horizontally:
            idx1 = 5
            idx2 = len (xsys [0][0]) - 5
        for x, y in xsys [1:]:
            result = add (result, x, y)
            #result += "{0} = {1}\n".format (y, x)
        return result

def load_data_sets (config_filename):
    """
    Load a configuration file specifying which data sets to use.
    The file should use a YAML format.
    The structure is:
    datasets:
    - {class: CLASS1, filename: FILENAME1}
    - {class: CLASS2, filename: FILENAME2}
    ...
    - {class: CLASSn, filename: FILENAMEn}
    has_header: BOOLEAN
    """
    with open (config_filename, "r") as fd:
        dictionary = yaml.load (fd)
        result = [DataSet (d ["filename"], d ["class"], dictionary ["has_header"]) for d in dictionary ["datasets"]]
    return result

def split_data_sets_train_test (list_data_sets, fraction_test, RNG):
    """

    :type RNG: numpy.random.RandomState
    :param list_data_sets:
    :param fraction_test:
    :return:
    """
    xs_splits = [d.split_two_sets (fraction_test, RNG) for d in list_data_sets]
    ys_splits = [(len (xs [0]) * [d.class_name], len (xs [1]) * [d.class_name]) for xs, d in zip (xs_splits, list_data_sets)]
    IDs_splits = [(len (xs [0]) * [d.class_ID], len (xs [1]) * [d.class_ID]) for xs, d in zip (xs_splits, list_data_sets)]
    result = {0: Function (), 1: Function ()}
    for xs, ys, IDs in zip (xs_splits, ys_splits, IDs_splits):
        for index in range (2):
            result [index].xs.extend (xs [index])
            result [index].ys.extend (ys [index])
            result [index].IDs.extend (IDs [index])
    return result [0], result [1]
