#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals # boilerplate
import unittest
from data_types import Lit, Clause
from random import randint

class TestLit(unittest.TestCase):
  def setUp(self):
    self.b = Lit(1)
    self.c = Lit(-1)
    self.d = Lit(2)

  def test_init(self):
    with self.assertRaises(ValueError):
      a = Lit(0)

  def test_is_complement(self):
    self.assertFalse(self.b.is_complement(self.d))
    self.assertTrue(self.b.is_complement(self.c))

class TestClause(unittest.TestCase):
  def setUp(self):
    self.a = Clause()
    for i in xrange(1, 6):
      self.a.add_var(i)
      self.a.add_var(-i)

  def test_size(self):
    self.assertEqual(self.a.size(), 10)

  def test_sort(self):
    shouldBe = [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5]
    self.a.my_sort() 
    self.assertEqual(self.a.to_list(), shouldBe)

    c = Clause() 
    c.add_var(5)
    c.add_var(-5)
    c.add_var(9)
    c.add_var(-6)
    c.add_var(-6)
    c.add_var(3)
    c.add_var(9)
    c.add_var(9)
    c.add_var(-2)
    c.my_sort()
    shouldBe = [-2, 3, -5, 5, -6, 9]
    self.assertEqual(c.to_list(), shouldBe)

  def test_irredundant(self):
    c = Clause() 
    c.add_var(5)
    c.add_var(-5)
    c.add_var(-5)
    c.add_var(-5)
    c.add_var(-6)
    c.add_var(3)
    c.add_var(9)
    c.add_var(9)
    c.add_var(-2)
    c.irredundant()
    c.my_sort()
    self.assertEqual(c.to_list(), [-2, 3, -5, 5, -6, 9])



def suite():
  suite = unittest.TestSuite()
  suite.addTest(TestLit('test_init'))
  suite.addTest(TestLit('test_is_complement'))
  suite.addTest(TestClause('test_size'))
  suite.addTest(TestClause('test_sort'))
  suite.addTest(TestClause('test_irredundant'))

  return suite

def main():
  unittest.TextTestRunner().run(suite())

if __name__=='__main__':
  main()
