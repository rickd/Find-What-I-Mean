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

        with self.assertRaises(TypeError):
            self.penalties.swap_cost(1, '1')
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('1', 1)
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('a', 'aa')
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('aa', 'a')


if __name__ == '__main__':
    unittest.main()
