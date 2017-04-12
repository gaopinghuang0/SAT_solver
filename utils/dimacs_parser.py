#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals # boilerplate
from data_types import Lit, Clause


def parse(filename, solver):
  var_num = None
  clause_num = None
  with open(filename, 'r') as f:
    for line in f.readlines():
      if line.startswith('p'):
        if var_num is not None:
          raise ValueError('only one line of p is allowed')
        _, cnf, var_num, clause_num = line.split()
      elif line.startswith('c'):
        pass
      else:
        clause = Clause()
        for v in line.split():
          if int(v) != 0:
            clause.add_var(v)
            solver.add_lit_type(Lit(v))
        solver.add_clause(clause)

  # solver._print()
  return solver


if __name__ == '__main__':
  def main():
    # parse('eg0.txt', )
    pass
    # class Test(object):
    #   def __init__(self, x=None):
    #     self.x = x or 1

    # t = Test()
    # print t.x

  main()
