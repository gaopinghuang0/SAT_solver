#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals # boilerplate
import time

# decorator for timing function performance
def timing(f):
    def wrap(*args):
        time1 = time.clock()
        ret = f(*args)
        time2 = time.clock()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap

if __name__ == '__main__':
  def main():
    pass

  main()
