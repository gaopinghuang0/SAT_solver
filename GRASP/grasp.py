#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals # boilerplate
from utils.data_types import *

DEBUG = False

def dbg(*kw):
  if DEBUG:
    print kw

class GRASP_Solver(object):
  def __init__(self, clauses=None):
    self.sat = STATUS_UNRES   # global status
    self.clauses = clauses or []  # store all Clauses
    self.assigns = {}  # e.g., {var: assign_value}
    self.tautology = []  # store tautology Clauses
    self.assign_stack = []   # a list of self-chosen branching variables, e.g., x1, x3, x7
    self.assign_graph = []   # a list of edges, e.g., [xi, xj] (xj is the implied var)
    self.prop_ok = False
    self.total_var_num = 0

  def init(self):
    res = set()
    for c in self.clauses:
      for value in c.to_list():
        res.add(abs(value))
    for var in res:
      self.assigns[var] = None

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

  def _print(self, verbose=False):
    if verbose:
      for c in self.clauses:
        c._print()
        
    if self.sat == STATUS_OK:
      print 'RESULT: SAT'
      print 'ASSIGNMENT:',
      for var, ass in self.assigns.iteritems():
        print 'x{}={}'.format(var, ass),
      print
    else:
      print 'RESULT: UNSAT'

  def update_status(self, c):
    """Check status for each clause based on self.assigns

    Affect:
      c.status, c.is_unit_clause, self.sat
    params:
      c: the clause to be checked
    """
    if c.status == STATUS_OK:
      return

    count = 0
    for lit in c.lits:
      var = lit.var
      # print var, self.assigns
      
      assign_value = self.assigns[var]
      var_result = lit.result(assign_value)
      if var_result == 1:
        c.status = STATUS_OK
        break
      elif var_result is None:
        count += 1
    if count == 0 and c.status != STATUS_OK:
      c.status = STATUS_FAIL
      self.sat = STATUS_FAIL
    if count == 1 and c.status != STATUS_OK:
      c.is_unit_clause = True
    else:
      c.is_unit_clause = False

  def get_imply(self, c, single_clause=False):
    """Find the only one var left in the unit clause and imply its value."""

    if single_clause:  # if single_clause, imply value regardless of current assign value
      lit = c.get_lit_by_index(0)
      return lit.var, 1 if lit.value > 0 else 0

    for lit in c.lits:
      var = lit.var
      assign_value = self.assigns[var]
      var_result = lit.result(assign_value)
      if var_result is None:
        return var, 1 if lit.value > 0 else 0

  def update_assigns(self, imply_var_dict):
    """Update self.assigns using imply_var_dict."""

    for var, imply_value in imply_var_dict.iteritems():
      self.assigns[var] = imply_value

  def build_graph(self, c):
    """Build the assign graph for unit clause.
    
    Find the only var left in the unit clause as the target of new edge.
    """
    if c.size() == 1:
      return

    target = None
    for lit in c.lits:
      var = lit.var
      assign_value = self.assigns[var]
      var_result = lit.result(assign_value)
      if var_result is None:
        target = var
        break
    if target:
      for lit in c.lits:
        if lit.var != target:
          self.assign_graph.append([lit.var, target])
    else:
      raise ValueError('target should not be None')


  def propogate(self):
    """BCP.
    
    Imply value for unit clause and propagate.
    """
    def is_validate(var, imply_value):
      if len(imply_var_dict) == 0:
        return True
      else:
        # only allow to store one imply var at one time
        if var not in imply_var_dict:
          return False
        return imply_var_dict[var] == imply_value

    imply_var_dict = {}
    sat_clause_count = 0
    for c in self.clauses:
      self.update_status(c)

      if c.status == STATUS_OK:
        sat_clause_count += 1
        continue
      # print c.to_list(), self.is_unit_clause(c), c.status, self.assigns, self.assign_stack
      # dbg(c.to_list(), c.is_unit_clause, self.assigns)

      if c.status == STATUS_FAIL:
        raise ValueError('should be able to detect conflict and not fail here')
      elif c.is_unit_clause:
        self.build_graph(c)
        var, imply_value = self.get_imply(c)
        # dbg(var, imply_value, self.assign_graph, is_validate(var, imply_value))
        # print self.assigns, var, imply_var_dict, is_validate(var, imply_value)
        if is_validate(var, imply_value):
          imply_var_dict[var] = imply_value
        else:
          if var in imply_var_dict:
            self.prop_ok = False
            self.conflict_var = var
            return
      else:
        pass

    if sat_clause_count == self.size():
      self.sat = STATUS_OK

    self.prop_ok = True
    return imply_var_dict
    # Avoid tail recursion
    # if len(imply_var_dict):
    #   # print 'imply_var_dict', imply_var_dict
    #   self.update_assigns(imply_var_dict)
    #   self.propogate()

  def set_next_var(self):
    """Pick the next var from self.assigns whose value is None."""

    found = False
    for var, assign in self.assigns.iteritems():
      if assign is None:
        if var in self.assign_stack:
          raise ValueError('should not be assigned')
        self.assign_stack.append(var)
        self.assigns[var] = 0
        found = True
        # print 'in set_next_var', var
        break
    return found

  def get_conflict_clause(self):
    """Get conflict clause based on conlict var and assign graph."""

    c = Clause()
    for edge in self.assign_graph:
      if edge[1] == self.conflict_var:
        c.add_var(edge[0])
    c.my_sort()
    return c

  def get_all_relevant_vars(self):
    """Span the assign graph to find all the vars that are relevant to the conflict var."""

    all_relevant_vars = set([self.conflict_var])
    var_stack = [self.conflict_var]
    while var_stack:
      var = var_stack.pop()
      for edge in self.assign_graph:
        if edge[1] == var:
          parent_var = edge[0]
          if parent_var not in all_relevant_vars:
            var_stack.append(parent_var)
            all_relevant_vars.add(parent_var)
    return all_relevant_vars

  def non_chronological_backtrack(self):
    '''Backtrack from the top of assign_stack 
        until the first var that is relevant to the conflict var and has value 0.
      Then change value from 0 to 1.
    '''
    all_relevant_vars = self.get_all_relevant_vars()
    # print self.conflict_var, all_relevant_vars, self.assign_stack, self.assigns
    back_var = None

    for var in self.assign_stack[::-1]:
      if var in all_relevant_vars:   # debug
        assign_value = self.assigns[var]
        if assign_value == 0:  # find one assign var with 0
          back_var = var
          break
    # print back_var
    return back_var

  def reset_all_clauses(self, back_var):
    """Reset all the vars of assign stack after back_var.

    reset assigns, remove from assign_stack, remove from assign_graph
    reset watch variables

    params:
      back_var: the var where backtrack process ends
    """
    index = None
    for ind, var in enumerate(self.assign_stack):
      if var == back_var:
        index = ind
        if self.assigns[var] == 0:
          self.assigns[var] = 1 
          self.assign_graph = [edge for edge in self.assign_graph \
          if var not in edge]  # remove from assign_graph
        else:
          raise ValueError('should be 0')
        
      if index and ind > index:   # reset each var that are after back_var
        self.assigns[var] = None
        self.assign_graph = [edge for edge in self.assign_graph \
          if var not in edge]  # remove from assign_graph

    self.assign_stack = self.assign_stack[:index+1]  # remove from assign_stack

    # reset the assign value of all vars that are not in assign_stack
    for var in self.assigns:
      if var not in self.assign_stack:
        self.assigns[var] = None

    for c in self.clauses:
      c.status = STATUS_UNRES
    # print 'after reset', self.assign_stack, self.assigns, self.assign_graph


  def has_next(self):
    """Pick next var to branch if any.
    
    Repeat propagating until convergence and then determine forward or backtracking.
    """
    if self.sat == STATUS_OK:
      return False

    imply_var_dict = self.propogate()
    while imply_var_dict:
      self.update_assigns(imply_var_dict)
      imply_var_dict = self.propogate()
      
    # dbg('prop_ok', self.prop_ok)
    if self.prop_ok:
      return self.set_next_var()
    else:  # has conflict or fail all
      c = self.get_conflict_clause()
      if c:
        self.add_clause(c)
        back_var = self.non_chronological_backtrack()
        if back_var:
          self.reset_all_clauses(back_var)
          return True
        else:
          self.sat = STATUS_FAIL
          return False

  def assign_dont_care_vars(self):
    """Assign value 0 to vars that did not appear in any clauses."""

    for var in xrange(1, self.total_var_num+1):
      if var not in self.assigns:
        self.assigns[var] = 0   # arbitrarily set it to 0

  def solve(self):
    """Entry function."""
    
    while self.has_next():
      pass

    if self.sat == STATUS_OK and len(self.assigns) < self.total_var_num:
      self.assign_dont_care_vars()

    return self.sat



if __name__ == '__main__':
  def main():
    pass

  main()
