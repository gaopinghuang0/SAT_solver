#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals # boilerplate


import sys, os, time

from random import randint
from time import sleep
from subprocess import call, Popen, PIPE

from DLL.dll import DLL_Solver
from GRASP.grasp import GRASP_Solver
from Chaff.chaff import Chaff_Solver

from utils.dimacs_parser import parse
from utils.file_generator import file_gen
from utils.utils import memory_usage_psutil

path = './benchmarks'

def solve(method, filename, verbose=True, timing=False, memory_usage=False):
  """ Solve a single file.

  params:
    vs_gold: compare our result with CHBR_glucose
    timing: show time spent
    memory_usage: show memory usage
  """

  if not filename:
    return

  if method == '-dll':
    solver = DLL_Solver()
  elif method == '-grasp':
    solver = GRASP_Solver()
  elif method == '-chaff':
    solver = Chaff_Solver()
  else:
    print 'unknown method'
    return

  parse(filename, solver)

  time1 = time.clock()
  solver.solve()
  time2 = time.clock()

  if timing:
    print 'solve function took %0.3f s' % ((time2-time1)*1.0)
  if memory_usage:
    memory_usage_psutil()
  
  if verbose:
    solver._print(False)

  return solver

def gen_n_random_file(n=1):
  """ Generate random benchmark files.
  
  params:
    n: number of files
  """
  for i in xrange(n):
    var = randint(10, 20)
    clause = randint(100, 1000)
    fn = 'random_v{}c{}.cnf'.format(var, clause)
    fn = os.path.join(path, fn)
    print 'generating {}'.format(fn)
    file_gen(fn, var, clause)


def compare_all(method, vs_gold=True, timing=True, memory_usage=True):
  """Solve all benchmarks

  Note: some files took too long using GRASP, so we simply skip them
  params:
    vs_gold: compare our result with CHBR_glucose
    timing: show time spent
    memory_usage: show memory usage
  """
  grasp_skip = ['random_v1087c7523.cnf', 'random_v242c2458.cnf', 'random_v65c982.cnf', 'random_v94c873.cnf']
  for dp, dn, filenames in os.walk(path):
    # if 'VarNum1000' in dp or 'VarNum100' in dp:  # hack to not run big test
    #   continue
    for f in filenames:
      fn = os.path.join(dp, f)
      if method == '-grasp' and f in grasp_skip:
        print '\nskip', fn
        continue
      print '\n{} solving {}'.format(method, fn)
      if vs_gold:
        # cmd = '~/ece595logic/CHBR_glucose_agile/bin/CHBR_glucose {} -model -verb=0'.format(fn)
        cmd = '~/ece595logic/CHBR_glucose_agile/bin/CHBR_glucose {} -verb=0'.format(fn)
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        out, err = p.communicate()

        solver = solve(method, fn, False, timing=timing, memory_usage=memory_usage)
        print 'SAT' if solver.sat else 'UNSAT'
        if solver.sat == 1 and 'UNSATISFIABLE' not in out:
          print 'ok'
        elif solver.sat == 0 and 'UNSATISFIABLE' in out:
          print 'ok'
        else:
          print 'not matched, our result is {}'.format(solver.sat) 
      else:
        solver = solve(method, fn, True, timing=timing, memory_usage=memory_usage)


def main():
  argv = sys.argv
  size = len(argv)
  try:
    is_timing = '-time' in argv
    is_mem_use = '-mem' in argv
    fn = filter(lambda x: not x.startswith('-'), argv[1:])
    if fn:
      f = fn[0]
    if '-gen' in argv:
      if size == 3:
        gen_n_random_file(int(argv[2]))
    elif '-all-vs-gold' in argv:
      if '-grasp' in argv:
        compare_all('-grasp', vs_gold=True)
      else:
        compare_all('-chaff', vs_gold=True)
    elif '-all' in argv:
      if '-grasp' in argv:
        compare_all('-grasp', vs_gold=False)
      else:
        compare_all('-chaff', vs_gold=False)
    elif '-grasp' in argv:
      solve('-grasp', f, True, timing=is_timing, memory_usage=is_mem_use)
    elif '-chaff' in argv:
      solve('-chaff', f, True, timing=is_timing, memory_usage=is_mem_use)
    else:
      # run chaff as default
      solve('-chaff', f, True, timing=is_timing, memory_usage=is_mem_use)
    return
  except Exception, e:
    print e
  
  print 'Usage: ./mySolver.py [-grasp, -chaff] [-time, -mem] <cnf file>'
  print 'OR: ./mySolver.py [-all, -all-vs-gold] [-grasp, -chaff]'

if __name__ == '__main__':
  main()
