#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals # boilerplate
from math import ceil

from GRASP.grasp import GRASP_Solver
from collections import Counter
from utils.data_types import *

DEBUG = False

ENABLE_VSIDS = True   # if enabled, pick the var with largest counter first and decay periodically
DECAY_RATIO = 1.4
DECAY_PERIOD = 10

def dbg(*kw):
  if DEBUG:
    print kw

def dbg_decay(*kw):
  if DEBUG and ENABLE_VSIDS:
    print kw

class Chaff_Solver(GRASP_Solver):
  def __init__(self, clauses=None):
    super(self.__class__, self).__init__()
    self.var_counter = Counter()  # count for each var among all clauses
    self.decay_ratio = 1

  def update_status(self, c):
    """ Overwrite GRASP update_status.
    Check status for each clause based on watch variables

    Affect:
      c.status, c.is_unit_clause, self.sat, c.watch
    params:
      c: the clause to be checked
    """
    def find_next_watch(lit_index):
      max_index = max(c.watch)
      for ind, lit in enumerate(c.lits):
        if ind > max_index and (self.assigns.get(lit.var) is None):
          c.watch.remove(lit_index)
          c.watch.append(ind)
          break

    def check_watch(watch_index):
      # dbg(c.watch, watch_index, c.lits)
      lit_index = c.watch[watch_index]
      watch_lit = c.get_lit_by_index(lit_index)
      assign_value = self.assigns.get(watch_lit.var)
      if assign_value is not None:
        if watch_lit.result(assign_value) == 1:
          c.status = STATUS_OK
          return True
        else:
          find_next_watch(lit_index)
          return False
      return None

    if c.status == STATUS_OK:
      return

    # check two watches of each clause
    # one watch is STATUS_OK, then no need to go further
    # or if two watches are both None, then no need to go further
    check1 = check_watch(0)
    check2 = check_watch(1)
    if check1 or check2:
      c.is_unit_clause = False
      return
    if check1 is None and check2 is None:
      c.is_unit_clause = False
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

  def set_next_var(self):
    """Pick the next var based on its counter and assign value to 0 if None."""
    found = False
    for var, count in self.var_counter.most_common():
      assign = self.assigns[var]
      if assign is None:
        if var in self.assign_stack:
          raise ValueError('should not be assigned')
        self.assign_stack.append(var)
        self.assigns[var] = 0
        found = True
        # print 'in set_next_var', var
        break
    return found

  def reset_all_clauses(self, back_var):
    """Reset all the vars of assign stack after back_var.

    Overwrite GRASP reset_all_clauses to also reset the watch variables

    params:
      back_var: the var where backtrack process ends
    """
    
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
      c.watch = [0, 1]
    # print 'after reset', self.assign_stack, self.assigns, self.assign_graph


  def has_next(self):
    """Pick next var to branch if any.
    
    Repeat propagating until convergence and then determine forward or backtracking.

    Overwrite GRASP has_next to preprocess single clause and update var counter.
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
        is_single_clause = c.size() == 1
        if is_single_clause:
          return self.preprocess()
        back_var = self.non_chronological_backtrack()
        if back_var:
          self.reset_all_clauses(back_var)
          if ENABLE_VSIDS:
            self.update_var_counter(c)
          return True
        else:
          self.sat = STATUS_FAIL
          return False

  def preprocess(self):
    """Preprocess single clauses.

    Imply value for single clause and then check for tautology or conflict
    """
    def is_validate(var, imply_value):
      # we allow multiple vars
      if var not in imply_var_dict:
        return True
      return imply_var_dict[var] == imply_value

    # check single clause assign imply value
    imply_var_dict = {}
    for c in self.clauses:
      if c.size() == 1:
        lit = c.get_lit_by_index(0)
        # imply value for single clause
        var, imply_value = self.get_imply(c, True)
        if is_validate(var, imply_value):
          imply_var_dict[var] = imply_value
        else:
          self.sat = STATUS_FAIL
          return False

    self.update_assigns(imply_var_dict)
    # remove all single clause if any
    if len(imply_var_dict):
      self.clauses = [c for c in self.clauses if c.size() > 1]

    # remove any clause that is sat or return Fail if one is Fail
    sat_index = []
    for index, c in enumerate(self.clauses):
      count = 0
      for lit in c.lits:
        var = lit.var
        assign_value = self.assigns[var]
        var_result = lit.result(assign_value)
        if var_result == 1:
          c.status = STATUS_OK
          sat_index.append(index)
          break
        elif var_result is None:
          count += 1
      if count == 0 and c.status != STATUS_OK:
        c.status = STATUS_FAIL
        self.sat = STATUS_FAIL
        return False
    
    if sat_index:
      self.clauses = [c for index, c in enumerate(self.clauses) if index not in sat_index]

    # init watch for each clause
    for c in self.clauses:
      c.watch = [0, 1]

    return True

  def update_var_counter(self, conflict_clause=None):
    """Update counter if conflict clause and decay periodically."""

    # we save the x and -x to the same counter
    counter = Counter()
    for c in self.clauses:
      if c.status == STATUS_UNRES:
        for lit in c.lits:
          counter[lit.var] += 1
    # dbg_decay('pre decay', counter)
    for cnt in counter:
      counter[cnt] = ceil(counter[cnt] / self.decay_ratio)
    # dbg_decay('after decay', counter)
    if conflict_clause:
      for lit in conflict_clause.lits:
        counter[lit.var] += 1
      # dbg_decay('add conflict', counter)

    self.var_counter = counter

  def decay_var_counter(self):
    self.decay_ratio *= DECAY_RATIO
    self.decay_ratio = min(self.size(), self.decay_ratio)
    # dbg_decay(self.decay_ratio)


  def solve(self):
    """Entry function."""
    if not self.preprocess():
      return STATUS_FAIL

    self.update_var_counter() # always init counter

    update_count = 0
    while self.has_next():
      update_count += 1
      if ENABLE_VSIDS and (update_count % DECAY_PERIOD == 0):
        self.decay_var_counter()


    if self.sat == STATUS_OK and len(self.assigns) < self.total_var_num:
      self.assign_dont_care_vars()

    return self.sat



if __name__ == '__main__':
  def main():
    pass

  main()
