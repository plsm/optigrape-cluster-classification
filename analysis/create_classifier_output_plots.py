import matplotlib
matplotlib.use ('Agg')
import csv
import matplotlib.pyplot
import math
import numpy
import sys

DECISION_TREE = 1
NEURAL_NETWORK = 2
GENETIC_PROGRAMING = 3

def create_classifier_output_plots (classifier, filename, long_classes_names, short_classes_names, plot_filename_suffix):
    """
    Create a figure with pie plots showing the output of the classifiers
    when presented with a record of a given class.  There is a pie for each
    class.  The pie slices show the classifier output: one for each of the
    specified classes, plus one pie used when the classifier produces no
    output.
    """
    number_classes = len (long_classes_names)
    if classifier is DECISION_TREE:
        sum_output = read_decision_tree_output (filename, number_classes)
    elif classifier is NEURAL_NETWORK:
        sum_output = read_neural_network_output (filename, number_classes)
    elif classifier is GENETIC_PROGRAMING:
        sum_output = read_genetic_programming_output (filename, number_classes)
    else:
        print ('Unrecognised classifier: {}!'.format (classifier))
        sys.exit (1)
    write_output (sum_output)
    write_confusion_matrix (sum_output, long_classes_names, short_classes_names, classifier is NEURAL_NETWORK, plot_filename_suffix)
    # plot artist attributes
    if classifier is DECISION_TREE or classifier is GENETIC_PROGRAMING:
        NO_OUTPUT = []
        labels = short_classes_names
        cmap = matplotlib.cm.rainbow (numpy.linspace (0.0, 1.0, number_classes))
        colors = cmap [range (number_classes)]
    elif classifier is NEURAL_NETWORK:
        NO_OUTPUT = ['no output']
        labels = short_classes_names + NO_OUTPUT
        cmap = matplotlib.cm.rainbow (numpy.linspace (0.0, 1.0, number_classes))
        colors = cmap [range (number_classes)]
        print (colors)
        gray = numpy.array ([[0.75, 0.75, 0.75, 1.0]])
        print (gray)
        colors = numpy.concatenate ((colors, gray))
        print (colors)
    # setup the figure
    golden_number = (1 + math.sqrt (5)) / 2
    number_rows = int (math.ceil (math.sqrt (number_classes + 1) / golden_number))
    number_cols = int (math.ceil (math.sqrt (number_classes + 1) * golden_number))
    while number_rows * (number_cols - 1) >= number_classes + 1:
        number_cols += -1
    margin_top = 0.6
    hspace = margin_top
    wspace = 0
    axes_size = 4
    figwidth = axes_size * number_cols + wspace * (number_cols - 1)
    figheight = axes_size * number_rows + margin_top + hspace * (number_rows - 1)
    figure = matplotlib.pyplot.figure (figsize = (figwidth, figheight), dpi = 300)
    array_axes = figure.subplots (
        nrows = number_rows,
        ncols = number_cols,
        gridspec_kw = {
            'wspace' : wspace / axes_size,
            'hspace' : hspace / axes_size,
            'left'   : 0,
            'right'  : 1,
            'top'    : (figheight - margin_top) / figheight,
            'bottom' : 0.0,
        }
    )
    # create the pie plots
    for index_class in range (number_classes):
        print ('Creating plot for {}'.format (long_classes_names [index_class]))
        ax = []
        labels_to_use = []
        colors_to_use = []
        explode = []
        total = sum (sum_output [index_class, :])
        for index_value, the_value in enumerate (sum_output [index_class, :]):
            if the_value > 0:
                ax.append (the_value)
                labels_to_use.append (labels [index_value])
                colors_to_use.append (colors [index_value])
                if float (the_value) / total < 0.03:
                    explode.append (0.2)
                else:
                    explode.append (0)
        an_axes = array_axes [index_class % number_rows, index_class / number_rows]
        an_axes.pie (
            ax,
            explode = explode,
            labels = labels_to_use,
            colors = colors_to_use,
            autopct = '%1.1f%%',
            radius = 0.75,
            pctdistance = 0.8
        )
        an_axes.set_title ('Predicted classes when classifier input is\n{}'.format (long_classes_names [index_class]))
    # setup a single axes showing the legend
    legend_axes = array_axes [number_classes % number_rows, number_classes / number_rows]
    legend_axes.legend (
        handles = [
            matplotlib.lines.Line2D (
                xdata = [0, 1],
                ydata = [1, 0],
                linestyle = 'solid',
                lw = 4,
                color = c)
            for c in colors
            ],
        labels = long_classes_names + NO_OUTPUT,
        loc = 'center',
        title = 'classifier output',
    )
    legend_axes.set_axis_off ()
    # clear the remaining axes
    for index_axes in range (number_classes + 1, number_rows * number_cols):
        an_axes = array_axes [index_axes % number_rows, index_axes / number_rows]
        an_axes.set_axis_off ()
    # save the figure
    figure.savefig ('classifier-output{}.jpg'.format (plot_filename_suffix))
    print ('Saved the plot')
    correct_sum = sum ([sum_output [i,i] for i in range (number_classes)])
    total = numpy.sum (sum_output)
    print ('Total success rate is {}%'.format (100.0 * correct_sum / float (total)))

def write_confusion_matrix (sum_output, long_classes_names, short_classes_names, has_no_output, html_table_filename_suffix):
    number_classes = len (long_classes_names)
    number_rows = number_classes + (1 if has_no_output else 0)
    filename = 'confusion-matrix_{}.html'.format (html_table_filename_suffix)
    fd = open (filename, 'w')
    fd.write ('''<html><head><style>
table      { border: none none solid solid 2pt;
             border-collapse: collapse;
             border-spacing: 15pt;
             empty-cells: hide;
             text-align: right }
td         { border: solid 1pt }
td.label { text-align: center }
td.special { border: none 2pt }  /* The top-left cell */
</style></head><body>''')
    fd.write ('<table>')
    fd.write ('<tr>')
    fd.write ('<td class="special" colspan="2" rowspan="2"></td>')
    fd.write ('<td colspan="{}" class="label">Actual Class</td>'.format (number_classes))
    fd.write ('</tr>\n')
    fd.write ('<tr>')
    for label in short_classes_names:
        fd.write ('<td class="label">{}</td>'.format (label))
    fd.write ('</tr>\n')
    for index_row in range (number_rows):
        fd.write ('<tr>')
        if index_row == 0:
            fd.write ('<td class="label" rowspan="{}">Predicted Class</td>'.format (number_rows))
        if index_row < number_classes:
            fd.write ('<td class="label">{}</td>'.format (long_classes_names [index_row]))
        else:
            fd.write ('<td class="label">no output</td>')
        for index_col in range (number_classes):
            fd.write ('<td>{}</td>'.format (sum_output [index_col, index_row]))
        fd.write ('</tr>\n')
    fd.write ('</table>')
    fd.write ('</body></html>')

    fd.close ()

def read_neural_network_output (filename, number_classes):
    # read the data
    with open (filename, 'r') as fdr:
        reader = csv.DictReader (fdr, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
        data = [row for row in reader]
    # check the data
    for row in data:
        if len (row) != 2 * number_classes:
            print ('Neural network output does not have {} classes! There is a row with {} values'.format (number_classes, len (row)))
            sys.exit (1)
    # compute the classifier output matrix
    result = numpy.zeros ((number_classes, number_classes + 1), dtype = numpy.int16)
    for row in data:
        real_class = None
        index = 1
        while True:
            if row ['real.class.{}'.format (index)] == 1:
                real_class = index
                break
            else:
                index += 1
        predicted_class = None
        for index in range (1, number_classes + 1):
            if row ['predicted.class.{}'.format (index)] == 1:
                predicted_class = index
                break
        if predicted_class is None:
            result [real_class - 1, number_classes] += 1
        else:
            result [real_class - 1, predicted_class - 1] += 1
    return result

def read_decision_tree_output (filename, number_classes):
    # read the data
    with open (filename, 'r') as fdr:
        reader = csv.DictReader (fdr, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
        data = [row for row in reader]
    # check the data
    for row in data:
        if len (row) != 2 or not (1 <= row ['real.class'] <= number_classes) or not (1 <= row ['predicted.class'] <= number_classes):
            print ('Decision tree output does not have {} classes! There is a row with {} values'.format (number_classes, len (row)))
            sys.exit (1)
    # compute the classifier output matrix
    result = numpy.zeros ((number_classes, number_classes + 1), dtype = numpy.int16)
    for row in data:
        real_class = int (row ['real.class'])
        predicted_class = int (row ['predicted.class'])
        result [real_class - 1, predicted_class - 1] += 1
    print (result)
    return result

def read_genetic_programming_output (list_filenames, number_classes):
    result = numpy.zeros ((number_classes, number_classes + 1), dtype = numpy.int16)
    for a_filename in list_filenames:
        # read the data
        with open (a_filename, 'r') as fdr:
            reader = csv.reader (fdr, delimiter = '\t', quoting = csv.QUOTE_NONNUMERIC, quotechar = '"')
            data = [row for row in reader]
        # compute the classifier output matrix
        for row in data:
            real_class = int (row [0])
            predicted_class = int (row [1])
            result [real_class - 1, predicted_class - 1] += 1
    print (result)
    return result

def write_output (output):
    numpy.savetxt (
        fname = 'classifier-output.csv',
        X = output,
        fmt = '%d',
        delimiter = ',',
    )
