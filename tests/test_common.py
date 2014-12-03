"""
Created on 24.08.2014

@author: evg-zhabotinsky

Common code for running TIRPAN tests.
"""

import os
import subprocess
import sys

atests_dir = os.path.dirname(__file__)  # Tests directory
tirpan_dir = os.path.join(atests_dir, '..')  # TIRPAN root directory

sys.path[1:1] = [tirpan_dir]

stdout = ''
stderr = ''

__old_hook__ = sys.excepthook
def __exception_hook__(*l, **d):
    """Hook that outputs TIRPAN's STDOUT and STDERR on failure"""
    sys.stderr.write('====STDOUT====\n')
    sys.stderr.write(stdout)
    sys.stderr.write('<=STDOUT END==\n')
    sys.stderr.write('====STDERR====\n')
    sys.stderr.write(stderr)
    sys.stderr.write('<=STDERR END==\n')
    sys.stderr.write('\nTEST FAILED\n')
    __old_hook__(*l, **d)
sys.excepthook = __exception_hook__

def do_tirpan(script_file, *args):
    """Get TIRPAN output (incl. stderr) for script

    Returns list of output lines (without newline chars).
    """

    # Run TIRPAN and capture STDOUT and STDERR
    global stdout, stderr
    proc = subprocess.Popen(['python',  # Windows refuses to run .py
                             os.path.join(tirpan_dir, 'tirpan.py'),
                             os.path.join(atests_dir, script_file)]
                             + list(args),
                            stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    proc.stdin.close()
    stdout = ''
    stderr = ''
    while proc.poll() is None:
        stdout += proc.stdout.read()
        stderr += proc.stderr.read()
    stdout += proc.stdout.read()
    stderr += proc.stderr.read()
    assert proc.returncode == 0,\
        'TIRPAN crashed (exit code {})'.format(proc.returncode)
    return (stdout + stderr).splitlines()


def assert_lines(output, correct_number):
    """Check if number of lines in output is correct

    Fail with corresponding message if not.
    """

    line_number = len(output)
    assert line_number == correct_number, (
        'there must be exactly {correct_number} line(s) in stderr, '
        'got {line_number} instead').format(**locals())
