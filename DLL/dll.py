#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals # boilerplate
import os, sys
sys.path.insert(0, os.path.abspath(".."))

from utils.data_types import *

class DLL_Solver(object):
  def __init__(self, clauses=None):
    self.sat = False 
    self.clauses = clauses or []
    self.assigns = []  # x1, x2, ..., xn
    self.lits_type = []
    self.current_assign_idx = 0

  def add_clause(self, clause):
    if not isinstance(clause, Clause):
      raise TypeError('type should be Clause')
    clause.my_sort()
    self.clauses.append(clause)

  def add_lit_type(self, lit):
    """
    Add lit tpye and update assigns during parsing.
    """
    if not isinstance(lit, Lit):
      raise TypeError('type should be Lit')
    lit.x = lit.x if lit.x > 0 else -lit.x
    if lit.x not in self .lits_type:
      self.lits_type.append(lit.x)
      self.assigns.append(None)
    self.lits_type.sort()

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
    
    _lits = map(lambda a: -a.x if a.x<0 else a.x, _lits)
    _lits = set(_lits)
    return _lits

  def check_sat(self):
    """
    Check if sat
    """
    
    if self.current_assign_idx > len(self.lits_type) - 1:
      self.current_assign_idx -= 1
      
    current_assign_idx = self.current_assign_idx
    assigns = self.assigns
    
    print assigns
    print "current_assign_idx ", current_assign_idx
    print assigns[current_assign_idx]
    if assigns[current_assign_idx] == None:
      assigns[current_assign_idx] = 0
      # self.current_assign_idx += 1
    elif assigns[current_assign_idx] == 0:
      assigns[current_assign_idx] = 1
      # self.current_assign_idx += 1
    else:
      
      self.current_assign_idx -= 1

    return self.sat

  def solve(self):
    while(not self.check_sat()):
      # assign_idx = 0
      # assign_val = self.assigns[assign_idx]
      current_assign_idx = self.current_assign_idx
      assign_val = self.assigns[current_assign_idx]
      assign_var_type = self.lits_type[current_assign_idx]
      sat_clause_count = 0
      for c in self.clauses:
        # c._print()
        status = c.status
        print c.status
        if status  == STATUS_OK: # Do not need to test if the clause is sat
          sat_clause_count += 1
          pass
        elif status == STATUS_UNRES: # Clasue unresolved
          var = c.lits[c.index]
          var_type = abs(var.x)
         
          if var_type == assign_var_type: # assign 1 or 0 to xn
            var_result = var.result(assign_val)
            if var_result == 1:
              c.status = STATUS_OK
            elif var_result == 0:
              c.status = STATUS_UNRES
              if assign_val == 1:
                c.index += 1
            # else:

          else: # the assignment is not current literal
            pass
         
        else: # Clause is not sat in current assign
          if self.current_assign_idx == -1:
            # Not sat
            return False
          else:
            # self.current_assign_idx -= 1
            pass
      if sat_clause_count == len(self.clauses):
        self.sat = True
      self.current_assign_idx += 1
    pass



if __name__ == '__main__':
  def main():
    pass

  main()
