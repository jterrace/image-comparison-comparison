import sys
import os
import tempfile
import subprocess

import util

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
        return pixels

class psnr(algo):
    name = 'PSNR'
    command = 'compare'
    
    def get_normval(self, srcpath, dstpath):
        tmpout = tempfile.mktemp()
        try:
            command = [self.binpath, '-metric', 'PSNR', srcpath, dstpath, tmpout]
            output = subprocess.check_output(command, stderr=subprocess.STDOUT)
            output = output.strip()
            return float(output)
        finally:
            os.remove(tmpout)

class rmse(algo):
    name = 'RMSE'
    command = 'compare'
    
    def get_normval(self, srcpath, dstpath):
        tmpout = tempfile.mktemp()
        try:
            command = [self.binpath, '-metric', 'RMSE', srcpath, dstpath, tmpout]
            output = subprocess.check_output(command, stderr=subprocess.STDOUT)
            output = output.strip()
            output = filter(lambda c: c != '(' and c != ')', output)
            output = output.split()[1]
            return float(output)
        finally:
            os.remove(tmpout)

ALGORITHMS = [
              pyssim(),
              perceptualdiff(),
              psnr(),
              rmse()
              ]
