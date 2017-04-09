#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals # boilerplate
import os, sys
sys.path.insert(0, os.path.abspath(".."))

from utils.data_types import Clause

class DLL_Solver(object):
  def __init__(self, clauses=None):
    self.clauses = clauses or []
    self.assigns = []  # x1, x2, ..., xn
  
  def add_clause(self, clause):
    if not isinstance(clause, Clause):
      raise TypeError('type should be Clause')
    self.clauses.append(clause)

  def _print(self):
    for c in self.clauses:
      c._print()

  def solve(self):
    pass



if __name__ == '__main__':
  def main():
    pass

  main()
