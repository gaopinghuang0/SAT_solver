#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals # boilerplate
from dll import DLL_Solver
from utils.dimacs_parser import parse



def main():
  solver = DLL_Solver()
  parse('../eg1.txt', solver)
  # solver._print()
  solver.solve()




if __name__ == '__main__':
  main()
