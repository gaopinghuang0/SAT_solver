#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals # boilerplate
import os, sys
sys.path.insert(0, os.path.abspath(".."))

from utils.data_types import *

class DLL_Solver(object):
  def __init__(self, clauses=None):
    self.sat = STATUS_UNRES
    self.clauses = clauses or []
    self.assigns = []  # x1, x2, ..., xn
    self.vars = []
    self.current_assign_idx = 0
    self.tautology = []

  def init(self):
    res = set()
    for c in self.clauses:
      for value in c.to_list():
        res.add(abs(value))
    self.vars = list(res)
    self.assigns = [None for _ in self.vars]
    self.vars.sort()

  def size(self):
    return len(self.clauses)

  def add_clause(self, clause):
    clause.my_sort()
    _lits = clause.to_list()
    if len(_lits) > len(set(map(abs, _lits))):
      self.tautology.append(clause)
      # print _lits, 'is tautology'
      return
    if not isinstance(clause, Clause):
      raise TypeError('type should be Clause')
    self.clauses.append(clause)

  def get_curr_var(self):
    return self.vars[self.current_assign_idx]

  def _print(self, verbose=False):

    if verbose:
      for c in self.clauses:
        c._print()
      print solver.current_assign_idx
        
    if self.sat == STATUS_OK:
      print 'RESULT: SAT'
      print 'ASSIGNMENT:',
      for var, ass in zip(self.vars, self.assigns):
        print 'x{}={}'.format(var, ass),
      print
    else:
      print 'RESULT: UNSAT'

  def reset_all_clauses(self):
    # reset current_assign_idx to the first 0 it met backwards
    i = self.current_assign_idx
    while i > -1:
      if self.assigns[i] == 1:
        self.assigns[i] = None
        i -= 1
      elif self.assigns[i] == 0:
        self.assigns[i] = 1
        # self.current_assign_idx = i
        break
      else:
        raise ValueError('should not be None when backtracking')
    # if i == -1:
    self.current_assign_idx = i
      # return

    # reset clause.index so that var is just more than assign_var
    # if clause.index -> var is larger than assign_var, reset to the first one that is more than assign var
    # otherwise, stay the same
    assign_var = self.get_curr_var()
    for c in self.clauses:
      lit = c.get_lit_by_index()
      if lit.var <= assign_var:
        continue
      else:
        for index, lit in enumerate(c.lits):
          if lit.var >= assign_var:
            c.index = index
            break


  def pick_next(self):
    if self.size() == 0:
      self.sat = STATUS_OK if self.tautology else STATUS_FAIL
      return False

    assign_value = self.assigns[self.current_assign_idx]

    sat_clause_count = 0
    fail_clause_count = 0
    for c in self.clauses:
      # if c.status == STATUS_UNRES:
      #   c._print()
      #   print c.index
      sat_clause_count += 1 if c.status == STATUS_OK else 0
      fail_clause_count += 1 if c.status == STATUS_FAIL else 0
    if sat_clause_count == self.size():
      self.sat = STATUS_OK
    if fail_clause_count == self.size():
      self.sat = STATUS_FAIL
    # print fail_clause_count

    if self.sat == STATUS_OK:
      return None
    elif self.sat == STATUS_FAIL:  # backwards
      if assign_value == 0:
        self.assigns[self.current_assign_idx] = 1
      elif assign_value == 1:
        self.reset_all_clauses()
      else:
        raise ValueError('should not be None when backtracking')
      self.sat = STATUS_UNRES
      return self.current_assign_idx >= 0
    else: # forwards when STATUS_UNRES
      if self.current_assign_idx < len(self.assigns)-1:
        if assign_value == 0 or assign_value == 1:
          self.current_assign_idx += 1
          self.assigns[self.current_assign_idx] = 0
        elif assign_value is None:
          self.assigns[self.current_assign_idx] = 0
      else:
        raise ValueError('should not be unres when all variables are assigned')
    return True

  def solve(self):
    while self.pick_next():
      current_assign_idx = self.current_assign_idx
      assign_value = self.assigns[current_assign_idx]
      assign_var = self.get_curr_var()
      # print self.assigns, assign_var, assign_value, current_assign_idx
      for c in self.clauses:
        lit = c.get_lit_by_index()
        if lit.var == assign_var:
          var_result = lit.result(assign_value)
          if var_result == 1:
            c.status = STATUS_OK
          elif var_result == 0:
            if c.index == c.size()-1:
              c.status = STATUS_FAIL
              self.sat = STATUS_FAIL
              break
            else:
              c.index += 1
              c.status = STATUS_UNRES

    return self.sat



if __name__ == '__main__':
  def main():
    pass

  main()
