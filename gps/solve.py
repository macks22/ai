"""
This module provides a CLI for the GPS which is capable of importing
a properly specified and solving it using the GPS.

"""
import os
import sys
import imp
import argparse
import logging

import gps


class NotModule(Exception):
    """Raise when path is specified for file which is not a Python module."""
    status_code = 1
    pass


class NoProblemFound(Exception):
    """Raise when no problem is found in specified module."""
    status_code = 2
    pass


def load_instance_from_file(klass, modpath):
    """Load an instance of klass from the module at modpath.

    :param str klass: The name of the class to find an instance of.
    :param str modpath: The path of the module to load an instance from.
    :return:  The first instance of klass found in the imported module.
    :raise NotModule: If modpath is not the path of a .py or .pyc file.

    """
    mod_name, file_ext = os.path.splitext(os.path.split(modpath)[-1])
    logging.info('attempting problem import from {} module'.format(mod_name))

    ext = file_ext.lower()
    if ext == '.py':
        py_mod = imp.load_source(mod_name, modpath)
    elif ext == '.pyc':
        py_mod = imp.load_compiled(mod_name, modpath)
    else:
        raise NotModule('{} is not Python source or bytecode'.format(modpath))

    for attr in dir(py_mod):
        mod_obj = getattr(py_mod, attr)
        if isinstance(mod_obj, klass):
            return mod_obj

    return None


def import_problem(modpath):
    """Import the first instance of :class:gps.Problem from the
    specified module path and return it.

    :rtype:  :class:gps.Problem
    :return: The imported problem.
    :raise NoProblemFound: If no instance of :class:gps.Problem was found
        in the module specified by modpath.

    """
    problem = load_instance_from_file(gps.Problem, modpath)
    if problem is None:
        raise NoProblemFound(
            'No instance of Problem was found in {}'.format(modpath))

    return load_instance_from_file(gps.Problem, modpath)


def solve(modpath):
    """Find the problem in the given module and solve it using the GPS.

    :param str modpath: Path of the python module with the problem
        specification (instance).

    """
    problem = import_problem(modpath)
    solver = gps.GPS()
    return solver.solve(problem)


def setup_parser():
    parser = argparse.ArgumentParser(
        description='Solve problems using the GPS.')

    parser.add_argument(
        'modpath', action='store',
        help='path of module with problem specification')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='print verbose output to console')

    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()

    if args.verbose:
        log_level = logging.INFO
    else:
        log_level = logging.ERROR

    logging.basicConfig(level=log_level)

    try:
        print solve(args.modpath)
    except (NotModule, NoProblemFound) as err:
        logging.error(str(err))
        return err.status_code

    return 0


if __name__ == "__main__":
    sys.exit(main())
