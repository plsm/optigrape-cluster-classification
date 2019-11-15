import argparse
import csv
import matplotlib.pyplot
import sklearn.tree._tree


def plot_histogram (histogram, attribute_labels, suffix, max_depth):
    figure = matplotlib.pyplot.figure (
        figsize=(12, 7),
        dpi=300)
    axes = figure.add_subplot (111)
    axes.bar (
        x=[i for i in range (len (histogram))],
        height=histogram,
        tick_label=attribute_labels,
    )
    axes.set_xlabel ('Kautsky curve time point')
    figure.suptitle (
        'Histogram of attribute usage in decision tree'
        '' if max_depth is None else '\nOnly decision tree nodes within {} hops from root node'.format (max_depth)
    )
    for t in axes.get_xticklabels ():
        t.set_fontsize ('xx-small')
        t.set_rotation ('vertical')
    figure.savefig ('histogram{}.png'.format (suffix))


def analyse_decision_trees (suffix, filenames, attribute_labels, max_depth):
    number_attributes = len (attribute_labels)
    histogram = [0] * number_attributes
    for filename in filenames:
        with open (filename, 'r') as fd:
            # print ('Processing {}...'.format (filename))
            freader = csv.reader (fd, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            for row in freader:
                number_nodes = int (row [2])
                depth = [0] * number_nodes
                for index_node in range (number_nodes):
                    child_left = int (row [3 + index_node])
                    child_right = int (row [3 + index_node + number_nodes])
                    attribute_index = int (row [3 + index_node + 2 * number_nodes])
                    if child_left != sklearn.tree._tree.TREE_LEAF:
                        depth [child_left] = depth [index_node] + 1
                    if child_right != sklearn.tree._tree.TREE_LEAF:
                        depth [child_right] = depth [index_node] + 1
                    if (child_left != sklearn.tree._tree.TREE_LEAF or child_right != sklearn.tree._tree.TREE_LEAF) \
                            and (max_depth is None or depth [index_node] < max_depth):
                        histogram [attribute_index] += 1
    useful_labels = [
        al if c > 0 else None
        for al, c in zip (attribute_labels, histogram)
    ]
    plot_histogram (
        histogram,
        useful_labels,
        suffix + ('' if max_depth is None else '_{}'.format (max_depth)),
        max_depth)


def main ():
    args = process_arguments()
    with open (args.attribute, 'r') as fd:
        freader = csv.reader (fd, delimiter='\t', quoting=csv.QUOTE_NONNUMERIC)
        attribute_labels = freader.__next__ ()
        print ('There are {} attributes'.format (len (attribute_labels)))
    for max_depth in [None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]:
        analyse_decision_trees (args.suffix, args.filename, attribute_labels, max_depth)


def process_arguments ():
    parser = argparse.ArgumentParser (
        description='Plot histogram of attribute usage in decision trees'
    )
    parser.add_argument (
        '-a',
        '--attribute',
        type=str,
        required=True,
        help='A filename containing a single line with the description of attributes, each separated by a TAB.',
    )
    parser.add_argument (
        '--suffix',
        type=str,
        default=None,
        help='A suffix to add to the png file containing the histogram.'
    )
    parser.add_argument (
        'filename',
        type=str,
        nargs='+',
        help='A CSV file containing decision trees, each one in a line.'
    )
    return parser.parse_args ()


main ()
