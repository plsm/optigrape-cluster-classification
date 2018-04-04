
import argparse
import zmq

import command_line_arguments
import socket_operations

class Master:
    def __init__ (self, args):
        print ("Creating socket to send requests...")
        self.sender = socket_operations.bind (zmq.PUSH, args.ventilator)
        print ("Creating socket to receive answers...")
        self.receiver = socket_operations.bind (zmq.PULL, args.sink)

    def loop (self):
        print ("Entering main loop...")
        self.hello_world()

    def hello_world (self):
        print ("Sending hello...")
        socket_operations.send (self.sender, "Hello")
        print ("Waiting for answer...")
        answer = socket_operations.recv (self.receiver)
        print (answer)

parser = argparse.ArgumentParser (
    description = "Optigrape master"
)
command_line_arguments.argument_sink (parser)
command_line_arguments.argument_ventilator (parser)
args = parser.parse_args ()
master = Master (args)
master.loop ()
