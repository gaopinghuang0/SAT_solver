#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals # boilerplate
import time
import os
import psutil

# decorator for timing function performance
# def timing(f):
#     def wrap(*args):
#         time1 = time.clock()
#         ret = f(*args)
#         time2 = time.clock()
#         print '%s function took %0.3f s' % (f.func_name, (time2-time1)*1.0)
#         return ret
#     return wrap

# Adapted from
# Credit: http://fa.bianp.net/blog/2013/different-ways-to-get-memory-consumption-or-lessons-learned-from-memory_profiler/
# Credit: http://stackoverflow.com/questions/938733/total-memory-used-by-python-process
def memory_usage_psutil():
    # return the memory usage in MB
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / float(2 ** 20)
    print '{0:.3f} MB'.format(mem)
    return mem


if __name__ == '__main__':
  def main():
    pass

  main()
