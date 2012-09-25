#!/usr/bin/env python2

import os
import json

import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import FuncFormatter
import numpy

import compare

CURDIR = os.path.dirname(os.path.abspath(__file__))

def main():
    with open(compare.OUTFILE, 'r') as f:
        data = json.load(f)
        algo_results = data['samples']
        run_results = data['run']
    
    rc('font', size='6')
    rc('font', family='serif')
    
    fig = plt.figure(figsize=(4, 2))
    
    positions = numpy.arange(len(compare.COMPARISONS)) + 0.2
    bar_width = 0.6
    
    colors = iter(['b', 'r', 'g', 'k', 'y', 'b', 'r', 'g'])
    for i, (algoname, algodata) in enumerate(algo_results.iteritems()):
        ax = fig.add_subplot(2, 2, i)
        color = next(colors)
        rects = ax.bar(positions, algodata, bar_width, color=color)
        ax.get_xaxis().set_visible(False)
        ax.set_title(algoname)
        plt.ylim((0, max(algodata) * 1.16))
        
        labels = ['M', 'C', 'I', 'B', 'J']
        
        def autolabel(rects):
            maxheight = max(rect.get_height() for rect in rects)
            for i, rect in enumerate(rects):
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2., height + 0.03 * maxheight, labels[i],
                        ha='center', va='bottom')
    
        autolabel(rects)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CURDIR, 'algo-comparison.pdf'))
    
    
    
    colors = iter(['b', 'r', 'g', 'k', 'y', 'b', 'r', 'g'])
    markers = iter(['s', 'p', 'o', 'v', '^', 'h'])
    fig = plt.figure(figsize=(4, 2))
    for i, (algoname, algodata) in enumerate(run_results.iteritems()):
        ax = fig.add_subplot(2, 2, i)
        color = next(colors)
        marker = next(markers)
        ax.plot(range(len(algodata)), algodata, color=color, marker=marker, markersize=2, linewidth=0.5, markeredgewidth=0.2)
        ax.set_title(algoname)
        if algoname == 'perceptualdiff':
            ax.yaxis.set_major_formatter(FuncFormatter(lambda v, pos: '%.0fK' % (v/1000.)))
        elif algoname == 'PSNR':
            plt.gca().invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(os.path.join(CURDIR, 'run-comparison.pdf'))

if __name__ == '__main__':
    main()
