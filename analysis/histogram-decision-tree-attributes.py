import csv
import sys
import sklearn.tree._tree

histogram = [0] * 118
print (histogram)
for filename in sys.argv [1:]:
    with open (filename, 'r') as fd:
        print ('Processing {}...'.format (filename))
        freader = csv.reader (fd, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for row in freader:
            # print (row)
            number_nodes = int (row [2])
            for index_node in range (number_nodes):
                attribute_index = int (row [3 + index_node + 2 * number_nodes])
                if attribute_index != sklearn.tree._tree.TREE_LEAF:
                    histogram [attribute_index] += 1
print (histogram)
