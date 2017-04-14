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
      print _lits, 'is tautology'
      return
    if not isinstance(clause, Clause):
      raise TypeError('type should be Clause')
    self.clauses.append(clause)

  def get_curr_var(self):
    return self.vars[self.current_assign_idx]

  def _print(self, verbose=False):
    for c in self.clauses:
      c._print()

    if verbose:
      print 'assigns:', self.assigns
      print 'vars:', self.vars
      # print solver.current_assign_idx
      print 'is SAT:', self.sat == STATUS_OK


  def reset_all_clauses(self):
    # reset current_assign_idx to the first 0 it met backwards
    i = self.current_assign_idx
    while i > -1:
      if self.assigns[i] == 1:
        self.assigns[i] = None
        i -= 1
      elif self.assigns[i] == 0:
        self.assigns[i] = 1
        self.current_assign_idx = i
        break
      else:
        raise ValueError('should not be None when backtracking')
    if i == -1:
      self.current_assign_idx = i
      return

    # reset clause.index so that var is no more than assign_var
    assign_var = self.get_curr_var()
    for c in self.clauses:
      for index, lit in enumerate(c.lits):
        if lit.var <= assign_var:
          c.index = index


  def pick_next(self):
    if self.size() == 0:
      self.sat = STATUS_OK if self.tautology else STATUS_FAIL
      return False

    assign_value = self.assigns[self.current_assign_idx]

    sat_clause_count = 0
    for c in self.clauses:
      sat_clause_count += 1 if c.status == STATUS_OK else 0
    if sat_clause_count == self.size():
      self.sat = STATUS_OK

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
    else: # forwards
      if self.current_assign_idx < len(self.assigns) - 1:
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
      print self.assigns, assign_var, assign_value, current_assign_idx
      for c in self.clauses:
        lit = c.get_lit_by_index()
        if lit.var == assign_var:
          var_result = lit.result(assign_value)
          if var_result == 1:
            c.status = STATUS_OK
          elif var_result == 0:
            if c.index == c.size()-1:
              c.staus = STATUS_FAIL
              self.sat = STATUS_FAIL
              break
            else:
              c.index += 1
              c.status = STATUS_UNRES

    return self.sat


  def solve_old(self):
    while(not self.check_sat()):
      # assign_idx = 0
      # assign_val = self.assigns[assign_idx]
      current_assign_idx = self.current_assign_idx
      assign_value = self.assigns[current_assign_idx]
      assign_var = self.get_curr_var()
      sat_clause_count = 0
      unsat_clause_count = 0
      unresolved_clause_count = 0
     
      print self.assigns
      print "current_assign_idx ", current_assign_idx

      for c in self.clauses:
        var = c.get_var_by_index()
        # c._print()
        status = c.status
        if status  == STATUS_OK: # Do not need to test if the clause is sat
          if self.downwards:
            sat_clause_count += 1
          else:
            if var == assign_var:
              pass
        elif status == STATUS_UNRES: # Clasue unresolved
          # print assign_var_type
          # print c.lits
          # print c.index
          # print "\n"
          # unresolved_clause_count += 1 
          if var == assign_var: # assign 1 or 0 to xn
            var_result = var.result(assign_value)
            if var_result == 1:
              c.status = STATUS_OK
              sat_clause_count += 1
            elif var_result == 0:
              c.status = STATUS_UNRES
              unresolved_clause_count += 1
              if c.index == c.size()-1:
                unsat_clause_count += 1
                c.staus = STATUS_FAIL
              else:
                c.index += 1
          else: # the assignment is not current literal
            unresolved_clause_count += 1
            c.status = STATUS_UNRES
            pass
         
        else: # Clause is not sat in current assign
          unsat_clause_count += 1
          
          if self.current_assign_idx == -1:
            return False
          else:
            pass
     
      # check sat condition
      print sat_clause_count, unresolved_clause_count, unsat_clause_count
      if sat_clause_count == len(self.clauses):
        self.sat = True
        return True
      elif unresolved_clause_count:
        if assign_value == 1:
          self.assigns[current_assign_idx] =None
          self.current_assign_idx -= 1
        else:
          self.current_assign_idx += 1
      elif unsat_clause_count:
        if (sat_clause_count+unsat_clause_count) == len(self.clauses):
          self.assigns[current_assign_idx] = None
          self.current_assign_idx -= 1
          if self.current_assign_idx == -1:
            return False



if __name__ == '__main__':
  def main():
    pass

  main()
