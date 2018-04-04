import pickle
import zmq

context = zmq.Context ()

def connect (type, server, port):
    result = context.socket (type)
    result.connect ("tcp://{0}:{1}".format (server, port))
    return result

def bind (type, port):
    result = context.socket (type)
    result.bind ("tcp://*:{0}".format (port))
    return result

def send (socket, data):
    data_bytes = pickle.dumps (data, -1)
    socket.send (data_bytes)

def recv (socket):
    """

    :rtype: object
    """
    data_bytes = socket.recv ()
    data = pickle.loads (data_bytes)
    return data

def send_recv (socket, data):
    send (socket, data)
    return recv (socket)
