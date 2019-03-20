import shlex
import subprocess
import sys
import os


def call_cmnd(cmnd='', verbose=False):
    if verbose is True:
        print '[i] calling', cmnd
    if len(cmnd) < 1:
        return '`[error] len(command) < 1 - this should not work.`'
    args = shlex.split(cmnd)
    try:
        p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
    except:
        e = sys.exc_info()
        out = '```{} Failed.```'.format(__name__)
        err = ('Error {0} : {1}').format(e[0], e[1])
        if verbose is True:
            print '[i]', out
            print '[e]', err
        return '\n'.join(['---', str(out), "", "Error details:", "```", str(err), "```", '---'])
    return str(out)


def test():
    return call_cmnd('date')


def cat_this():
    fname, ext = os.path.splitext(__file__)
    if ext == '.pyc':
        fname = fname + '.py'
    else:
        fname = __file__
    with open(fname) as f:
        cl = f.readlines()
    cl.insert(0, '#!python\n')
    cl.insert(0, '```\n')
    cl.append('```\n')
    return ''.join(cl)
