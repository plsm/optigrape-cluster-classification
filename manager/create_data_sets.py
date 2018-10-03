#!/usr/bin/python

import argparse
import os
import os.path
import yaml

def main ():
    args = parse_arguments ()
    list_data_sets = [
        (os.path.abspath (f), os.path.basename (f))
        for f in args.FILE
        if os.path.exists (os.path.abspath (f))
    ]
    for f in args.FILE:
        if not os.path.exists (f):
            print ('[W] File {} does not exist!'.format (f))
    if len (list_data_sets) == 0:
        print ('[W] No data files to process!')
    list_data_sets = process_labels (list_data_sets)
    if args.decision_tree:
        create_data_sets_for_decision_tree (args, list_data_sets)
    if args.pairwise:
        for index, (a_data_set_file, a_label) in enumerate (list_data_sets [:-2]):
            for (b_data_set_file, b_label) in list_data_sets [(index + 1):]:
                if args.neural_network:
                    dict = {
                        'datasets': [
                            {
                                'filename' : a_data_set_file,
                                'class' : [1, 0]
                            },
                            {
                                'filename': b_data_set_file,
                                'class': [0, 1]
                            },
                        ]
                    }
                    filename = 'NN_{}{}_VS_{}{}.dataset'.format (
                        args.prefix,
                        a_label,
                        b_label,
                        args.suffix,
                    )
                    with open (filename, 'w') as fdw:
                        yaml.dump (dict, fdw)
    if args.all:
        if args.neural_network:
            data = {
                'datasets' : [
                    {
                        'filename': a_data_set_file,
                        'class' : index * [0] + [1] + (len (list_data_sets) - index - 1) * [0]
                    }
                    for index, (a_data_set_file, _a_label) in enumerate (list_data_sets)
                ]
            }
            filename = 'NN_{}ALL{}.dataset'.format (
                args.prefix,
                args.suffix,
            )
            with open (filename, 'w') as fdw:
                yaml.dump (data, fdw)

def create_data_sets_for_decision_tree (args, list_data_sets):
    if args.all:
        write_data_sets_file (
            data = {
                'datasets': [
                    {
                        'filename': a_data_set_file,
                        'class': [index + 1]
                    }
                    for index, (a_data_set_file, _a_label) in enumerate (list_data_sets)
                ]
            },
            filename = 'DT_{}ALL{}'.format (
                args.prefix,
                args.suffix
            )
        )
    if args.pairwise:
        for index, (a_data_set_file, a_label) in enumerate (list_data_sets [:-2]):
            for (b_data_set_file, b_label) in list_data_sets [(index + 1):]:
                write_data_sets_file (
                    data = {
                        'datasets': [
                            {
                                'filename' : a_data_set_file,
                                'class' : [1]
                            },
                            {
                                'filename': b_data_set_file,
                                'class': [2]
                            },
                        ]
                    },
                    filename = 'DT_{}{}_VS_{}{}.dataset'.format (
                        args.prefix,
                        a_label,
                        b_label,
                        args.suffix,
                    )
                )

def write_data_sets_file (data, filename):
    with open (filename, 'w') as fdw:
        yaml.dump (data, fdw)

def process_labels (list_data_sets):
    prefix_index = 0
    suffix_index = 0
    go = True
    stop_prefix = False
    stop_suffix = False
    while go:
        if not stop_prefix: prefix_index += 1
        if not stop_suffix: suffix_index += -1
        common_prefix = list_data_sets [0][1][:prefix_index]
        common_suffix = list_data_sets [0][1][suffix_index:]
        for _, a_label in list_data_sets [1:]:
            if not stop_prefix and a_label [:prefix_index] != common_prefix:
                stop_prefix = True
                prefix_index += -1
            if not stop_suffix and a_label [suffix_index:] != common_suffix:
                stop_suffix = True
                suffix_index += 1
        go = not stop_suffix or not stop_prefix
    return [
        (a_data_set_file, a_label [prefix_index:suffix_index])
        for a_data_set_file, a_label in list_data_sets
    ]

def parse_arguments ():
    parser = argparse.ArgumentParser (
        description = 'Read a set of files containing data set classes and generate .dataset files for the classifier algorithms.'
    )
    parser.add_argument (
        'FILE',
        type = str,
        nargs = '*',
        help = 'file with a data set'
    )
    parser.add_argument (
        '--pairwise',
        action = 'store_true',
        help = 'generate .dataset files containing pairs of the supplied data sets'
    )
    parser.add_argument (
        '--all',
        action = 'store_true',
        help = 'generate a .dataset file containing all the supplied data sets'
    )
    parser.add_argument (
        '--neural-network',
        action = 'store_true',
        help = 'generate .dataset files for the neural network classifier algorithm.  The filename starts by NN.'
    )
    parser.add_argument (
        '--decision-tree',
        action = 'store_true',
        help = 'generate .dataset files for the decision tree classifier algorithm.  The filename starts by DT.'
    )
    parser.add_argument (
        '--suffix',
        type = str,
        metavar = 'LABEL',
        default = '',
        help = 'suffix to add to the generate .dataset files'
    )
    parser.add_argument (
        '--prefix',
        type = str,
        metavar = 'LABEL',
        default = '',
        help = 'prefix to add to the generate .dataset files'
    )
    return parser.parse_args ()

if __name__ == '__main__':
    main ()
