#!/usr/bin/env python2

import os
import sys
import subprocess

import util

CURDIR = os.path.dirname(os.path.abspath(__file__))
DATADIR = os.path.join(CURDIR, 'data')

COMPARISONS = (
    ('Blur', 'einstein.gif', 'blur.gif'),
    ('Contrast', 'einstein.gif', 'contrast.gif'),
    ('Impulse', 'einstein.gif', 'impulse.gif'),
    ('JPG', 'einstein.gif', 'jpg.gif'),
    ('Meanshift', 'einstein.gif', 'meanshift.gif'),
)

class algo(object):
    def __init__(self):
        self.binpath = util.which(self.command)
        if self.binpath is None:
            sys.stderr.write("Could not find program '%s'. Ensure that it is on the path. Exiting.\n" % self.command)
            sys.exit(1)
        sys.stdout.write("Found '%s' at '%s'\n" % (self.name, self.binpath))
        
    def get_normval(self, srcpath, dstpath):
        raise NotImplementedError()

class pyssim(algo):
    name = 'SSIM'
    command = 'pyssim'
    
    def get_normval(self, srcpath, dstpath):
        output = subprocess.check_output([self.binpath, srcpath, dstpath])
        output = output.strip()
        value = float(output)
        return 1.0 - value

class perceptualdiff(algo):
    name = 'perceptualdiff'
    command = 'perceptualdiff'
    
    def get_normval(self, srcpath, dstpath):
        command = [self.binpath, '-threshold', '1', srcpath, dstpath]
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retcode = p.wait()
        if retcode == 0:
            # no output, return code 0 means identical images
            return 0.
        lastline = p.stdout.read().strip().split('\n')[-1]
        pixels = lastline.split()[0]
        pixels = int(pixels)
        return pixels / (256. * 256.)

ALGORITHMS = [
              pyssim(),
              perceptualdiff()
              ]

def main():
    for testname, orig, mod in COMPARISONS:
        origpath = os.path.join(DATADIR, orig)
        modpath = os.path.join(DATADIR, mod)
        print testname
        for algo in ALGORITHMS:
            normval = algo.get_normval(origpath, modpath)
            print '\t', algo.name, normval

if __name__ == '__main__':
    main()
