import argparse
import zmq

import command_line_arguments
import socket_operations

class Worker:
    def __init__ (self, args):
        print ("Creating socket to receive requests...")
        self.receiver = socket_operations.connect (zmq.PULL, args.server, args.ventilator)
        print ("creating socket to send answers...")
        self.sender = socket_operations.connect (zmq.PUSH, args.server, args.sink)

    def loop (self):
        print ("Entering main loop")
        self.hello_world ()

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
args = parser.parse_args ()
worker = Worker (args)
worker.loop ()
