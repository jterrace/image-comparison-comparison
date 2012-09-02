#!/usr/bin/env python2

import os
import json
import collections

import algorithms

CURDIR = os.path.dirname(os.path.abspath(__file__))
DATADIR = os.path.join(CURDIR, 'data')
OUTFILE = os.path.join(CURDIR, 'data.json')

COMPARISONS = (
    ('Blur', 'einstein.gif', 'blur.gif'),
    ('Contrast', 'einstein.gif', 'contrast.gif'),
    ('Impulse', 'einstein.gif', 'impulse.gif'),
    ('JPG', 'einstein.gif', 'jpg.gif'),
    ('Meanshift', 'einstein.gif', 'meanshift.gif'),
)

def main():
    algo_results = collections.defaultdict(list)
    for testname, orig, mod in COMPARISONS:
        origpath = os.path.join(DATADIR, orig)
        modpath = os.path.join(DATADIR, mod)
        print testname
        for algo in algorithms.ALGORITHMS:
            normval = algo.get_normval(origpath, modpath)
            algo_results[algo.name].append(normval)
            print '\t', algo.name, normval
    
    groundtruth_files = sorted(os.listdir(os.path.join(DATADIR, 'groundtruth')))
    realtime_files = sorted(os.listdir(os.path.join(DATADIR, 'realtime')))
    
    run_results = collections.defaultdict(list)
    for groundtruth_file, realtime_file in zip(groundtruth_files, realtime_files):
        groundtruth_file = os.path.join(DATADIR, 'groundtruth', groundtruth_file)
        realtime_file = os.path.join(DATADIR, 'realtime', realtime_file)
        print os.path.basename(groundtruth_file)
        for algo in algorithms.ALGORITHMS:
            normval = algo.get_normval(groundtruth_file, realtime_file)
            run_results[algo.name].append(normval)
            print '\t', algo.name, normval
    
    with open(OUTFILE, 'w') as f:
        json.dump({'samples':algo_results,
                   'run': run_results}, f, indent=2)
    
    print
    print 'Results written to', OUTFILE
    print

if __name__ == '__main__':
    main()
