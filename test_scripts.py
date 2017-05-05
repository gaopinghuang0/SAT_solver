#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals # boilerplate


import sys, os

from random import randint
from time import sleep
from subprocess import call, Popen, PIPE

from DLL.dll import DLL_Solver
from GRASP.grasp import GRASP_Solver
from Chaff.chaff import Chaff_Solver

from utils.dimacs_parser import parse
from utils.file_generator import file_gen


path = './benchmarks'

def solve(method, filename, verbose=True):
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
  # print '#'*6, 'before', '#'*6
  # solver._print(False)

  solver.solve()
  # print '#'*6, 'after', '#'*6
  if verbose:
    solver._print(False)

  return solver

def gen_n_random_file(n=1):
  for i in xrange(n):
    var = randint(10, 20)
    clause = randint(100, 1000)
    fn = 'random_v{}c{}.cnf'.format(var, clause)
    fn = os.path.join(path, fn)
    print 'generating {}'.format(fn)
    file_gen(fn, var, clause)

def compare_all():
  for dp, dn, filenames in os.walk(path):
    for f in filenames:
      fn = os.path.join(dp, f)
      print '\ntesting ', fn
      # cmd = '~/ece595logic/CHBR_glucose_agile/bin/CHBR_glucose {} -model -verb=0'.format(fn)
      cmd = '~/ece595logic/CHBR_glucose_agile/bin/CHBR_glucose {} -verb=0'.format(fn)
      p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
      out, err = p.communicate()

      solver = solve('-chaff', fn, False)
      print solver.sat
      if solver.sat == 1 and 'UNSATISFIABLE' not in out:
        print 'ok'
      elif solver.sat == 0 and 'UNSATISFIABLE' in out:
        print 'ok'
      else:
        print 'not matched, our result is {}'.format(solver.sat) 

      sleep(1)
    # for debug
    break



def main():
  argv = sys.argv
  if len(argv) == 2:
    if argv[1] == '-all':
      compare_all()
      return
    elif not argv[1].startswith('-'):
      # run default
      solve('-chaff', argv[1])
      return
  elif len(argv) == 3:
    method = argv[1]
    if method in ['-dll', '-grasp', '-chaff']:
      solve(method, argv[2], True)
    elif method == '-gen':
      gen_n_random_file(int(argv[2]))
    return
  
  print 'Usage: python test_script.py [-dll, -grasp, -chaff] <cnf file>'
  print 'OR: python test_script.py -all'

if __name__ == '__main__':
  main()
