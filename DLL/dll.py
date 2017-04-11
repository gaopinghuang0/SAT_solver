#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals # boilerplate
import os, sys
sys.path.insert(0, os.path.abspath(".."))

from utils.data_types import Clause, Lit

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

  def get_lits_type(self):
    """
    Get whole lit types in this solver,
    and sort them in order
    """
    _lits = []
    for c in self.clauses:
      _lits += c.to_list()
    _lits = map(lambda x:Lit(x), set(_lits))      
    _lits.sort(key=lambda a:a.x) 
    _lits.sort(key=lambda a:abs(a.x))
    return _lits

  def check_sat(self):
    """
    Check if sat
    """
    sat = 0
    for c in self.clauses:
      sat *= c.status
    return sat

  def solve(self):
    lits_type = self.get_lits_type()

    for assign_idx, assign_val in enumerate(self.assigns):
    while(check_sat() is None):
      assign_idx = 0
      self.assigns[assign_idx] = 0
      assign_val = self.assigns[assign_idx]
      for c in self.clauses:
        c.my_sort()
        c._print()
        if c.STATUS_OK:
          pass
        else:
          var_type = abs(c.lits[c.index])/2
          var = c.lits[c.index]
          if var_type == assign_idx: #assign 1 or 0 to xn
            var_result = var.result(assign_val)
          if var_result == 1:
            c.status = STATUS_OK
          c.index += 1
          if (c.index == c.size) and (c.status == STATUS_UNRES):
            c.status = STATUS_FAIL
      assign_idx += 1

    pass



if __name__ == '__main__':
  def main():
    pass

  main()
