"""IP address where the ventilator and sink process are running."""
SERVER = "192.92.149.171"

"""Port number used by the ventilator to send requests to the workers."""
VENTILATOR = 4557

"""Port number used by the sink to receive results from the workers."""
SINK = 4558

def argument_server (parser):
    parser.add_argument (
        "--server",
        type = str,
        default = SERVER,
        metavar = "HOST",
        help = "IP address where the ventilator and sink process are running"
    )

def argument_ventilator (parser):
    parser.add_argument (
        "--ventilator",
        type = int,
        default = VENTILATOR,
        metavar = "PORT",
        help = "port number used by the ventilator to send requests to the workers"
    )

def argument_sink (parser):
    parser.add_argument (
        "--sink",
        type = int,
        default = SINK,
        metavar = "PORT",
        help = "port number used by the sink to receive results from the workers"
    )

def data_set (parser):
    parser.add_argument (
        "--data-set",
        metavar = "PATH",
        type = str,
        action = "append",
        required = True,
        help = "filename path containing the data set of a class.  Each class is in its own file."
    )
