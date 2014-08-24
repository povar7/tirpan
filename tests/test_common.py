"""
Created on 24.08.2014

@author: evg-zhabotinsky

Common code for running TIRPAN tests.
"""

import os
import subprocess

atests_dir = os.path.dirname(__file__)  # Tests directory (contains this module)
tirpan_dir = os.path.join(atests_dir, '..')  # TIRPAN root directory


def do_tirpan(script_file):
    """Get TIRPAN output (incl. stderr) for script

    Returns list of output lines (without newline chars).
    """

    # Run TIRPAN and capture STDOUT and STDERR
    output = subprocess.check_output(['python',  # Windows refuses to run .py
                                      os.path.join(tirpan_dir, 'tirpan.py'),
                                      os.path.join(atests_dir, script_file)],
                                     stderr=subprocess.STDOUT)
    return output.splitlines()


def assert_lines(output, correct_number):
    """Check if number of lines in output is correct

    Fail with corresponding message if not.
    """

    line_number = len(output)
    assert line_number == correct_number, (
        'there must be exactly {correct_number} line(s) in stderr, '
        'got {line_number} instead').format(**locals())
