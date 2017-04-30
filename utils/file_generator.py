#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals # boilerplate
from random import randint

def file_gen(filename, var_num, clause_num):
  content = []
  with open(filename, 'wb') as f:
    content.append('c Here is a file called '+filename)
    content.append('p cnf {} {}'.format(var_num, clause_num))
    for _ in xrange(clause_num):
      data = []
      for j in xrange(randint(1, var_num)):
        data.append((-1)**randint(0, 2) * randint(1, var_num))
      content.append(' '.join(map(str, data)) + ' 0')

    f.write('\n'.join(content))


if __name__ == '__main__':
  def main():
    file_gen('../benchmarks/random_v40c300.1.cnf', 20, 100)

  main()
