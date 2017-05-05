#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals # boilerplate
from utils.data_types import *
from utils.utils import timing

DEBUG = False

def dbg(*kw):
  if DEBUG:
    print kw

class GRASP_Solver(object):
  def __init__(self, clauses=None):
    self.sat = STATUS_UNRES
    self.clauses = clauses or []
    self.assigns = {}  # {var: assign_value}
    self.tautology = []
    self.assign_stack = []   # e.g., x1, x3, x7
    self.assign_graph = []   # each edge [xi, xj] in which xj is implied var
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
    """find the only one var left in the unit clause and imply its value"""
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
    for var, imply_value in imply_var_dict.iteritems():
      self.assigns[var] = imply_value

  def build_graph(self, c):
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
    """implication"""
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
      dbg(c.to_list(), c.is_unit_clause, self.assigns)

      if c.status == STATUS_FAIL:
        raise ValueError('should be able to detect conflict and not fail here')
      elif c.is_unit_clause:
        self.build_graph(c)
        var, imply_value = self.get_imply(c)
        dbg(var, imply_value, self.assign_graph, is_validate(var, imply_value))
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
    if len(imply_var_dict):
      # print 'imply_var_dict', imply_var_dict
      self.update_assigns(imply_var_dict)
      self.propogate()

  def set_next_var(self):
    """"""
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
    # print 'conflict_var', self.conflict_var
    c = Clause()
    for edge in self.assign_graph:
      if edge[1] == self.conflict_var:
        c.add_var(edge[0])
    c.my_sort()
    return c

  def non_chronological_backtrack(self, c):
    '''relevant vars should be in the conflict clause
      back track from the top of assign_stack
    '''
    all_relevant_vars = map(abs, c.to_list())
    back_var = None

    for var in self.assign_stack[::-1]:
      if var in all_relevant_vars:
        assign_value = self.assigns[var]
        if assign_value == 0:  # find one assign var with 0
          back_var = var
          break
    return back_var

  def reset_all_clauses(self, back_var):
    """reset assigns, remove from assign_stack, remove from assign_graph"""
    # print 'before reset', self.assign_stack, self.assigns, self.assign_graph
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
    if self.sat == STATUS_OK:
      return False

    self.propogate()
    dbg('prop_ok', self.prop_ok)
    if self.prop_ok:
      return self.set_next_var()
    else:  # has conflict or fail all
      c = self.get_conflict_clause()
      if c:
        self.add_clause(c)
        back_var = self.non_chronological_backtrack(c)
        if back_var:
          self.reset_all_clauses(back_var)
          return True
        else:
          self.sat = STATUS_FAIL
          return False

  def assign_dont_care_vars(self):
    for var in xrange(1, self.total_var_num+1):
      if var not in self.assigns:
        self.assigns[var] = 0   # arbitrarily set it to 0

  @timing
  def solve(self):
    while self.has_next():
      print self.assigns
      print self.assign_stack
      pass

    if self.sat == STATUS_OK and len(self.assigns) < self.total_var_num:
      self.assign_dont_care_vars()

    return self.sat



if __name__ == '__main__':
  def main():
    pass

  main()
