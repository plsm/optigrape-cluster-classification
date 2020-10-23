# plot Kautsky curves
# this script accepts a series of filenames and labels

from __future__ import print_function

import argparse
import matplotlib
import matplotlib.pyplot
import os.path
import sys

import classifier.dataset

TIMESTAMPs = [0.00001, 0.00002, 0.00003, 0.00004, 0.00005, 0.00006, 0.00007, 0.00008, 0.00009, 0.0001, 0.00011, 0.00012, 0.00013, 0.00014, 0.00015, 0.00016, 0.00017, 0.00018, 0.00019, 0.0002, 0.00021, 0.00022, 0.00023, 0.00024, 0.00025, 0.00026, 0.00027, 0.00028, 0.00029, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.0009, 0.001, 0.0011, 0.0012, 0.0013, 0.0014, 0.0015, 0.0016, 0.0017, 0.0018, 0.0019, 0.002, 0.0021, 0.0022, 0.0023, 0.0024, 0.0025, 0.0026, 0.0027, 0.0028, 0.0029, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.011, 0.012, 0.013, 0.014, 0.015, 0.016, 0.017, 0.018, 0.019, 0.02, 0.021, 0.022, 0.023, 0.024, 0.025, 0.026, 0.027, 0.028, 0.029, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

TS_DEFAULT = 'default'
TS_ABSTRACT = 'abstract'

def main ():
    args = process_arguments ()
    if not args.with_header and not args.no_header:
        print ('You should provide one of the --with-header or --no-header arguments')
        sys.exit (1)
    elif args.with_header and args.no_header:
        print ('Conflicting arguments: -with-header and --no-header')
        sys.exit (0)
    # user provided labels
    labels = args.label [:len (args.data_set)]
    # default labels are computed from dataset filenames
    labels += [
        os.path.basename (a_data_set_filename)
        for a_data_set_filename in args.data_set [len (args.label):]
    ]
    list_figs_axes = []
    def new_figure (label):
        result_figure = matplotlib.pyplot.figure (figsize = (14, 9))
        result_axes = result_figure.add_subplot (111)
        list_figs_axes.append ((result_figure, result_axes, label))
        return result_axes
    compare_axes = new_figure ('compare')
    max_y = 0
    for a_label, a_data_set in zip (labels, args.data_set):
        single_axes = new_figure (a_label)
        d = classifier.dataset.DataSet (a_data_set, a_label, has_header = args.with_header)
        xs = []
        ys = []
        for row in d.rows:
            if args.timestamps == TS_DEFAULT:
                xs.extend (TIMESTAMPs)
            elif args.timestamps == TS_ABSTRACT:
                xs.extend ([t for t in range (len (row))])
            ys.extend (row)
        max_y = max ([max_y, max (ys)])
        pc = compare_axes.scatter (xs, ys, marker = '.', label = a_label, alpha = 0.25)
        single_axes.scatter (xs, ys, marker = '.', label = a_label, alpha = 0.25, c = pc.get_facecolor ())
        single_axes.set_title(a_label, fontsize = 24)
    for fig, axa, a_label in list_figs_axes:
        axa.legend ()
        if args.timestamps == 'default':
            axa.set_xlabel ('time (s)')
        elif args.timestamps == 'abstract':
            axa.set_xlabel ('time')
            axa.set_xticklabels ([])
        axa.set_ylabel ('intensity (a.u.)')
        axa.set_ylim (-52, max_y + 200)
        fig.show ()
        fig.savefig (a_label + '.png')
    print ('Press ENTER to finish')
    raw_input ('> ')

def process_arguments ():
    parser = argparse.ArgumentParser (
        description = 'Plot Kautsky curves from several data-sets.  Each data-set has a distinct name and label.  By default, the label is the filename.'
    )
    parser.add_argument (
        '--data-set', '-d',
        type = str,
        required = True,
        action = 'append',
        metavar = 'PATH',
        help = 'Text file containing Kautsky effect data.'
    )
    parser.add_argument (
        '--label', '-l',
        type = str,
        default = [],
        action = 'append',
        metavar = 'STRING',
        help = 'the n-th occurrence of this argument is used as a label for the n-th occurrence of the -d argument.'
    )
    parser.add_argument (
        '--with-header',
        action = 'store_true',
        help = 'The text files with data have a header row'
    )
    parser.add_argument (
        '--no-header',
        action = 'store_true',
        help = 'The text files with data do not have a header row'
    )
    parser.add_argument (
        '--timestamps',
        type = str,
        choices = [TS_DEFAULT, TS_ABSTRACT],
        required = True,
        help = '''What kind of timestamps to use:
        default     use hard coded timestamps
        abstract    use abstract timestamps'''
    )
    return parser.parse_args ()

if __name__ == '__main__':
    main ()
