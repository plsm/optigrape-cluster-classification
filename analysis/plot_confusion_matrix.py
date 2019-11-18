#!/usr/bin/env python3
import argparse
import csv
import sys
from typing import List

import matplotlib.pyplot
import numpy
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels


ORDER_TRUE_PREDICTED = 'true-predicted'
ORDER_PREDICTED_TRUE = 'predicted-true'


def main (list_files_name, order, suffix):
    # y_predicted, y_true = read_data (list_files_name, order)
    y_predicted, y_true = read_nn_data (list_files_name)
    print (y_predicted)
    print (y_true)
    plot_confusion_matrix (
        y_true=y_true,
        y_pred=y_predicted,
        # classes=[str (i) for i in range (1, 8)],
        classes=[
            'no output',
            'vitis vinifera cv\ncabernet sauvignon',
            'vitis labrusca cv\nisabella',
            'vitis vinifera cv\npinot noir',
            'vitis vinifera cv\nriesling',
            'vitis riparia cv riparia\ngloire de montpellier',
            'vitis rupestris\ndu lot',
            'vitis vinifera cv\ntrincadeira',
        ],
        normalize=True,
        suffix=suffix,
    )


def plot_confusion_matrix (
        y_true, y_pred, classes,
        suffix=None,
        normalize=False,
        title=None,
        cmap=matplotlib.pyplot.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    # classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, numpy.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)
    cm = cm [1:, :]
    print (cm)
    figure = matplotlib.pyplot.figure (
        figsize=(7, 7),
        dpi=300)
    axes = figure.add_subplot (111)
    if normalize:
        im = axes.imshow(cm, interpolation='nearest', cmap=cmap, vmin=0, vmax=1)
    else:
        im = axes.imshow (cm, interpolation='nearest', cmap=cmap)
    axes.figure.colorbar(im, ax=axes)
    # We want to show all ticks...
    axes.set(
        xticks=numpy.arange(cm.shape[1]),
        yticks=numpy.arange(cm.shape[0]),
        # ... and label them with the respective list entries
        xticklabels=classes,
        yticklabels=classes [1:],
        title=title,
        ylabel='True class',
        xlabel='Predicted class')

    # Rotate the tick labels and set their alignment.
    matplotlib.pyplot.setp (
        axes.get_xticklabels(),
        rotation=45,
        ha="right",
        rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            axes.text(
                j, i, format(cm[i, j], fmt),
                ha="center",
                va="center",
                color="white" if cm[i, j] > thresh else "black")
    figure.tight_layout ()
    figure.savefig (
        'confusion-matrix.png' if suffix is None else
        'confusion-matrix_{}.png'.format (suffix))
    return axes


def read_data (list_files_name: List[str], order: str):
    all_data = None
    for filename in list_files_name:
        contents = numpy.loadtxt (
            fname=filename,
            dtype=int,
            skiprows=0,
            # delimiter=', \t',
        )
        if all_data is None:
            all_data = contents
        else:
            all_data = numpy.concatenate ((all_data, contents))
    if order == ORDER_TRUE_PREDICTED:
        y_true = all_data [:, 0]
        y_predicted = all_data [:, 1]
    elif order == ORDER_PREDICTED_TRUE:
        y_true = all_data[:, 1]
        y_predicted = all_data[:, 0]
    else:
        raise AssertionError ('Not reached')
    return y_predicted, y_true


def read_nn_data (list_files_name: List[str]):
    all_data = None
    for filename in list_files_name:
        contents = read_neural_network_output (filename, 7)
        if all_data is None:
            all_data = contents
        else:
            all_data = numpy.concatenate ((all_data, contents))
    y_true = all_data[:, 1]
    y_predicted = all_data[:, 0]
    return y_predicted, y_true


def read_neural_network_output (filename, number_classes):
    # read the data
    with open (filename, 'r') as fdr:
        reader = csv.DictReader (
            fdr,
            delimiter=',',
            quoting=csv.QUOTE_NONNUMERIC,
            quotechar='"')
        data = [row for row in reader]
    # check the data
    for row in data:
        if len (row) != 2 * number_classes:
            print ('Neural network output does not have {} classes! There is a row with {} values'.format (
                number_classes,
                len (row)))
            sys.exit (1)
    result = []
    for row in data:
        real_class = -1
        for index in range (1, number_classes + 1):
            if row ['real.class.{}'.format (index)] == 1:
                real_class = index
                break
        predicted_class = 0
        for index in range (1, number_classes + 1):
            if row ['predicted.class.{}'.format (index)] == 1:
                predicted_class = index
                break
        result.append ((predicted_class, real_class))
    return numpy.array (result)


def process_arguments ():
    parser = argparse.ArgumentParser (
        description='Plot confusion matrices'
    )
    parser.add_argument (
        '--order',
        choices=[ORDER_TRUE_PREDICTED, ORDER_PREDICTED_TRUE],
        required=True,
        help='The order that predicted and expected classes appear in each line of the CSV files.'
    )
    parser.add_argument (
        '--suffix',
        metavar='LABEL',
        default=None,
        help='A suffix to add to the filename with the confusion matrix.'
    )
    parser.add_argument (
        'filename',
        type=str,
        nargs='+',
        help='A CSV file containing in one column the predicted class and in another column the expected class.'
    )
    return parser.parse_args ()


if __name__ == '__main__':
    args = process_arguments ()
    main (args.filename, args.order, args.suffix)
