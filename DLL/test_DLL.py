#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals # boilerplate
from dll import DLL_Solver
from utils.dimacs_parser import parse



def main():
  solver = DLL_Solver()
  parse('../eg0.txt', solver)
  solver._print()
  solver.solve()
  print solver.assigns
  print solver.lits_type


if __name__ == '__main__':
  main()
