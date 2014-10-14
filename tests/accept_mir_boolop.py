#!/usr/bin/env python

"""
Created on 14.10.2014

@author: evg-zhabotinsky

Run all tests related to MIR generation for boolean expressions
"""

def do_check(lines, correct):
    import re
    blocks = dict()
    block = dict()
    # print '===> Lines'
    # for line in lines:
    #     print line
    it = iter(lines)
    line = next(it)
    while not line or line.strip('='):
        line = next(it)
    line = next(it)
    while True:
        while not line:
            line = next(it)
        if not line.strip('='):
            break
        m = re.match('#BLOCK (\d+)$', line)
        assert m
        block['id'] = m.group(1)
        line = next(it)
        aliases = dict()
        while True:
            m = re.match('([^# ]+) = (.+)$', line)
            if not m:
                break
            l, r = m.groups()
            r = aliases.get(r, r)
            aliases[l] = r
            line = next(it)
        block['aliases'] = aliases
        m = re.match('#IF ([^ ]+)$', line)
        if m:
            v = m.group(1)
            block['cond'] = aliases.get(v, v)
            line = next(it)
            m = re.match('#THEN (\d+)$', line)
            assert m
            block['goto'] = m.group(1)
            line = next(it)
            m = re.match('#ELSE (\d+)$', line)
            assert m
            block['else'] = m.group(1)
            line = next(it)
        else:
            block['cond'] = None
            m = re.match('#GOTO (\d+)$', line)
            if m:
                block['goto'] = m.group(1)
                line = next(it)
            else:
                block['goto'] = None
                assert line == '#RETURN'
                line = next(it)
        assert not line
        blocks[block['id']] = block
        block = dict()
    assert not block
    # print '===> Blocks'
    # for i, block in blocks.items():
    #     print i, ':', block
    # print '===> Correct'
    rules = dict()
    result = None
    for line in correct:
        m = re.match('(\d+) *\? *(\d+|T|F|R) *: *(\d+|T|F|R)', line)
        if m:
            l, r = m.group(2, 3)
            rules[m.group(1)] = {'goto':l, 'else':r}
        else:
            m = re.match('R *: *([^ ]*)', line)
            assert m
            result = m.group(1)
        # print line
    assert result
    # print '===> Rules'
    # print 'Result :', result
    # for i, rule in rules.items():
    #     print i, ':', rule
    # print '===> End'
    blocks_by_cond = dict()
    cnt = 0
    for i, block in blocks.items():
        if block['aliases'].get(result, None) == 'True':
            assert not block['cond']
            assert not blocks_by_cond.has_key('T')
            blocks_by_cond['T'] = block
        elif block['aliases'].get(result, None) == 'False':
            assert not block['cond']
            assert not blocks_by_cond.has_key('F')
            blocks_by_cond['F'] = block
        elif not block['goto']:
            assert not block['cond']
            assert not blocks_by_cond.has_key('R')
            blocks_by_cond['R'] = block
        else:
            assert block['cond']
            assert not blocks_by_cond.has_key(block['cond'])
            blocks_by_cond[block['cond']] = block
            cnt += 1
    # print 'True : ', blocks_by_cond.get('T', None)
    # print 'False : ', blocks_by_cond.get('F', None)
    # print 'Return : ', blocks_by_cond['R']
    # for i, block in blocks.items():
    #     print i, ':', block
    # print
    for i, rule in rules.items():
        assert blocks_by_cond[i]['goto'] == blocks_by_cond[rule['goto']]['id']
        assert blocks_by_cond[i]['else'] == blocks_by_cond[rule['else']]['id']
        # print i, ':', rule, '-- OK'
        cnt -= 1
    assert cnt == 0
    assert not blocks_by_cond.has_key('T') \
        or blocks_by_cond['T']['goto'] == blocks_by_cond['R']['id']
    assert not blocks_by_cond.has_key('F') \
        or blocks_by_cond['F']['goto'] == blocks_by_cond['R']['id']
    return True

from test_common import *
import sys

tests_subdir = 'mir_boolop'
tests_dir = os.path.join(atests_dir, tests_subdir)
for fname in os.listdir(tests_dir):
    name, ext = os.path.splitext(fname)
    if ext == '.py':
        try:
            lines = do_tirpan(os.path.join(tests_subdir, fname), '--mir-only')
            with open(os.path.join(tests_dir, name + '.txt')) as f:
                correct = f.read().splitlines()
            assert do_check(lines, correct)
        except :
            sys.stderr.write('Checking problem at {}:\n'.format(
                os.path.join(tests_subdir, fname)))
            raise
