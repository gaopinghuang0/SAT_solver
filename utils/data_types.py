#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals # boilerplate

STATUS_OK = 1
STATUS_FAIL = 0
STATUS_UNRES = None

class Lit(object):
  def __init__(self, x):
    if x == 0:
      raise ValueError('literal should not be 0')
    self.x = int(x)

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return str(self.x)

  def is_complement(self, other):
    return self.x + other.x == 0

  def result(self, assign):
    """
    assign: 0 or 1
    if self.x > 0, return assign
    if self.x < 0, return 1 if assign == 0 else 0
    """
    if self.x > 0:
      return assign
    elif assign == 0:
      return 1
    else:
      return 0

  @property
  def var(self):
    "the i-th variable"
    return abs(self.x)

  @property
  def value(self):
    return self.x



class Clause(object):
  def __init__(self, lits=None):
    self.lits = lits or []
    self.index = 0
    self.status = STATUS_UNRES
    
  def add_var(self, p):
    if isinstance(p, Lit):
      self.lits.append(p)
    else:
      self.lits.append(Lit(p))

  def _print(self):
    print self.to_list()

  def irredundant(self):
    _lits = []
    for x in set(self.to_list()):
      _lits.append(Lit(x))
    self.lits = _lits

  def to_list(self):
    return [a.value for a in self.lits]

  def my_sort(self):
    """
    The sorted order:  -x1, x1, -x2, x2, -x3, x3, ...
    -1, 1, -2, 2, -3, 3, ...
    """
    self.irredundant()
    self.lits.sort(key=lambda a: a.x)
    self.lits.sort(key=lambda a: abs(a.x))

  def size(self):
    return len(self.lits)

  def get_lit_by_index(self, index=None):
    return self.lits[self.index if index is None else index]

  def is_last(self):
    return self.index == self.size - 1



if __name__ == '__main__':
  def main():
    pass

  main()
