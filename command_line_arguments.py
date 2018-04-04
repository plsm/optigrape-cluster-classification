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
        help = "IP address where the ventilator and sink process are running"
    )

def argument_ventilator (parser):
    parser.add_argument (
        "--ventilator",
        type = int,
        default = VENTILATOR,

        help = "port number used by the ventilator to send requests to the workers"
    )

def argument_sink (parser):
    parser.add_argument (
        "--sink",
        type = int,
        default = SINK,
        help = "port number used by the sink to receive results from the workers"
    )
