import argparse
import zmq

import command_line_arguments
import dataset
import socket_operations

class Worker:
    def __init__ (self, args):
        print ("Creating socket to receive requests...")
        self.receiver = socket_operations.connect (zmq.PULL, args.server, args.ventilator)
        print ("creating socket to send answers...")
        self.sender = socket_operations.connect (zmq.PUSH, args.server, args.sink)
        print ("loading data sets...")
        print (args.data_set)
        self.list_data_sets = self.load_data_sets (args.data_set)

    def loop (self):
        print ("Entering main loop")
        for d in self.list_data_sets:
            print ("OI")
            print (d)
        return None

    def load_data_sets (self, list_file_names):
        # type: (list(str)) -> object
        return [dataset.DataSet (filename) for filename in list_file_names]

    def hello_world (self):
        print ("Waiting for request...")
        request = socket_operations.recv (self.receiver)
        print ("Sending answer...")
        socket_operations.send (self.sender, request + "I'm the worker")

parser = argparse.ArgumentParser (
    description = "Optigrape worker"
)
command_line_arguments.argument_server (parser)
command_line_arguments.argument_sink (parser)
command_line_arguments.argument_ventilator (parser)
command_line_arguments.data_set (parser)
args = parser.parse_args ()
worker = Worker (args)
worker.loop ()
