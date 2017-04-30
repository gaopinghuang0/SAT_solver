#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals # boilerplate
from dll import DLL_Solver
from utils.dimacs_parser import parse



def main():
  solver = DLL_Solver()
  parse('../benchmarks/random_v20c100.cnf', solver)
  # print '#'*6, 'before', '#'*6
  # solver._print(True)

  solver.solve()
  # print '#'*6, 'after', '#'*6
  # solver._print(True)
  print solver.sat




if __name__ == '__main__':
  main()
