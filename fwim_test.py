#!/usr/bin/python3 -tt

#    Tests the finder system.
#    Copyright (C) 2011 Rick Dangerous
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import fwim

class TestBasicPenalties(unittest.TestCase):
    
    def setUp(self):
        self.penalties = fwim.BasicPenalties()

    def test_positivity(self):
        self.assertTrue(self.penalties.get_transpose_penalty() >= 0)
        self.assertTrue(self.penalties.get_drop_penalty() >= 0)
        self.assertTrue(self.penalties.get_add_penalty() >= 0)
        self.assertTrue(self.penalties.get_swap_penalty() >= 0)

    def test_swap_cost(self):
        self.assertEqual(0, self.penalties.swap_cost('a', 'a'))
        self.assertEqual(self.penalties.get_swap_penalty(),
                         self.penalties.swap_cost('b', 'c'))
        self.assertEqual(self.penalties.swap_cost('c', 'b'),
                         self.penalties.swap_cost('b', 'c'))
        self.assertEqual(self.penalties.swap_cost('a', 'b'),
                         self.penalties.swap_cost('a', 'c'))
        self.assertEqual(self.penalties.swap_cost('a', 'b'),
                         self.penalties.swap_cost('c', 'd'))

    def test_bad_input(self):
        with self.assertRaises(TypeError):
            self.penalties.swap_cost(1, '1')
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('1', 1)
        with self.assertRaises(TypeError):
            self.penalties.swap_cost(1, 1)
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('a', 'aa')
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('aa', 'a')
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('aa', 'aa')
        with self.assertRaises(TypeError):
            self.penalties.swap_cost(None, 'a')
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('a', None)

class TestDistanceEvaluator(unittest.TestCase):

    def setUp(self):
        self.penalties = fwim.DistinctPenalties()
        self.dev = fwim.EditDistanceEvaluator(self.penalties)

    def test_identity(self):
        self.assertEqual(self.dev.distance('', ''), 0)
        self.assertEqual(self.dev.distance('a', 'a'), 0)
        self.assertEqual(self.dev.distance('asdf1234', 'asdf1234'), 0)

    def test_bad_input(self):
        with self.assertRaises(TypeError):
            self.dev.distance('a', None)
        with self.assertRaises(TypeError):
            self.dev.distance(None, 'a')
        with self.assertRaises(TypeError):
            self.dev.distance(None, None)
        
        with self.assertRaises(TypeError):
            self.dev.distance('a', 1)
        with self.assertRaises(TypeError):
            self.dev.distance(1, 'a')
        with self.assertRaises(TypeError):
            self.dev.distance(1, 1)

    def test_single_errors(self):
        self.assertEqual(self.dev.distance('', ''), 0)
        self.assertEqual(self.dev.distance('', 'a'),
                         self.penalties.get_add_penalty())
        self.assertEqual(self.dev.distance('', '123456'),
                         6*self.penalties.get_add_penalty())

        self.assertEqual(self.dev.distance('abc', 'abcd'),
                         self.penalties.get_add_penalty())
        self.assertEqual(self.dev.distance('abc', 'dabc'),
                         self.penalties.get_add_penalty())
        self.assertEqual(self.dev.distance('abc', 'adbc'),
                         self.penalties.get_add_penalty())
        self.assertEqual(self.dev.distance('abc', 'abdc'),
                         self.penalties.get_add_penalty())

        self.assertEqual(self.dev.distance('a', ''),
                         self.penalties.get_drop_penalty())
        self.assertEqual(self.dev.distance('123456', ''),
                         6*self.penalties.get_drop_penalty())
        self.assertEqual(self.dev.distance('abc', 'bc'),
                         self.penalties.get_drop_penalty())
        self.assertEqual(self.dev.distance('abc', 'ac'),
                         self.penalties.get_drop_penalty())
        self.assertEqual(self.dev.distance('abc', 'ab'),
                         self.penalties.get_drop_penalty())

        self.assertEqual(self.dev.distance('abc', 'bbc'),
                         self.penalties.get_swap_penalty())
        self.assertEqual(self.dev.distance('abc', 'aac'),
                         self.penalties.get_swap_penalty())
        self.assertEqual(self.dev.distance('abc', 'abb'),
                         self.penalties.get_swap_penalty())

        self.assertEqual(self.dev.distance('abc', 'acb'),
                         self.penalties.get_transpose_penalty())
        self.assertEqual(self.dev.distance('abc', 'bac'),
                         self.penalties.get_transpose_penalty())
        self.assertEqual(self.dev.distance('abcd', 'acbd'),
                         self.penalties.get_transpose_penalty())

    def test_multiple_errors(self):
        # http://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
        self.assertEqual(self.dev.distance('ca', 'abc'),
                         self.penalties.get_drop_penalty() + 
                         2*self.penalties.get_add_penalty())

        self.assertEqual(self.dev.distance('abcdefg', 'acbdeg'),
                         self.penalties.get_transpose_penalty() +
                         self.penalties.get_drop_penalty())

        self.assertEqual(self.dev.distance('abcdefg', 'acbdefgz'),
                         self.penalties.get_transpose_penalty() +
                         self.penalties.get_add_penalty())

        
if __name__ == '__main__':
    unittest.main()
