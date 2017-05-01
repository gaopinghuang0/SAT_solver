#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals # boilerplate


import sys, os

from random import randint
from time import sleep
from subprocess import call

from DLL.dll import DLL_Solver
from GRASP.grasp import GRASP_Solver

from utils.dimacs_parser import parse
from utils.file_generator import file_gen



path = './benchmarks'

def dll_solve(filename):
  if not filename:
    return

  solver = DLL_Solver()
  parse(filename, solver)
  # print '#'*6, 'before', '#'*6
  # solver._print(False)

  solver.solve()
  # print '#'*6, 'after', '#'*6
  solver._print(False)

def grasp_solve(filename):
  if not filename:
    return

  solver = GRASP_Solver()
  parse(filename, solver)
  # print '#'*6, 'before', '#'*6
  # solver._print(False)

  solver.solve()
  # print '#'*6, 'after', '#'*6
  solver._print(False)


def gen_n_random_file(n=1):
  for i in xrange(n):
    var = randint(10, 100)
    clause = randint(100, 1000)
    fn = 'random_v{}c{}.cnf'.format(var, clause)
    fn = os.path.join(path, fn)
    print 'generating {}'.format(fn)
    file_gen(fn, var, clause)

def compare_all():
  for f in os.listdir(path):
    fn = os.path.join(path, f)
    print '\ntesting ', fn
    cmd = '~/ece595logic/CHBR_glucose_agile/bin/CHBR_glucose {} -model -verb=0'.format(fn)
    call(cmd, shell=True)

    grasp_solve(fn)
    sleep(1)



def main():
  argv = sys.argv
  if len(argv) == 2:
    if argv[1] == '-all':
      compare_all()
    elif not argv[1].startswith('-'):
      # run default
      dll_solve(argv[1])
      return
  elif len(argv) == 3:
    method = argv[1]
    if method == '-dll':
      dll_solve(argv[2])
    elif method == '-grasp':
      grasp_solve(argv[2])
    elif method == '-gen':
      gen_n_random_file(int(argv[2]))
    return
  
  print 'Usage: python test_script.py [-dll, -grasp, -chaff] <cnf file>'
  print 'OR: python test_script.py -all'

if __name__ == '__main__':
  main()
