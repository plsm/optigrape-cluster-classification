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

def data_sets_file (parser):
    parser.add_argument (
        "--data-sets",
        metavar = "PATH",
        type = str,
        required = True,
        help = "text file containing pairs of data sets and their classes."
    )

def learning_parameters_file (parser):
    parser.add_argument (
        "--learning-parameters",
        metavar = "PATH",
        type = str,
        required = True,
        help = "text file containing the parameters of the classifier algorithm."
    )

def fraction_test (parser):
    parser.add_argument (
        "--fraction-test",
        type = float,
        required = True,
        metavar = "X",
        help = "Fraction of the data set to be used as test set"
    )

def number_repeats (parser):
    parser.add_argument (
        "--number-repeats",
        type = int,
        default = 30,
        metavar = "N",
        help = "how many repeats to perform"
    )

def RNG_seed (parser):
    parser.add_argument (
        "--RNG-seed",
        type = int,
        required = True,
        metavar = "N",
        help = "Pseudo-random number generator seed"
    )


def arguments_neural_network (parser):
    parser.add_argument (
        "--hidden-layer-size",
        type = int,
        action = "append",
        required = True,
        default = [],
        help = "The ith occurrence of this argument represents the number of neurons in the ith hidden layer."
    )
    parser.add_argument (
        "--activation",
        type = str,
        choices = ["identity", "logistic", "tanh", "relu"],
        default = "tanh",
        help = """Activation function for the hidden layer(s).

            identity, no-op activation, useful to implement linear bottleneck, returns f(x) = x
            logistic, the logistic sigmoid function, returns f(x) = 1 / (1 + exp(-x)).
            tanh, the hyperbolic tan function, returns f(x) = tanh(x).
            relu, the rectified linear unit function, returns f(x) = max(0, x)
    """)
    parser.add_argument (
        "--solver",
        type = str,
        choices = ["lbfgs", "sgd", "adam"],
        default = "lbfgs",
        help = "The solver for weight optimisation."
    )
    parser.add_argument (
        "--alpha",
        type = float,
        default = 1e-5
    )
    parser.add_argument (
        "--max-iterations",
        type = int,
        default = 200,
        help = """Maximum number of iterations. The solver iterates until convergence (determined by 'tol') or this number of iterations. For stochastic solvers ('sgd', 'adam'), note that this determines the number of epochs (how many times each data point will be used), not the number of gradient steps."""
    )
    parser.add_argument (
        "--early-stopping",
        type = bool,
        default = False,
        help = "Whether to use early stopping to terminate training when validation score is not improving. If set to true, it will automatically set aside 10% of training data as validation and terminate training when validation score is not improving by at least tol for two consecutive epochs. Only effective when solver=sgd or adam"
    )
