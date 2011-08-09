#!/usr/bin/python3 -tt
# -*- coding: UTF-8 -*-

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
        with self.assertRaises(TypeError):
            self.penalties.swap_cost(None, None)


class TestCustomSwapPenalties(unittest.TestCase):

    def setUp(self):
        self.penalties = fwim.CustomSwapPenalties()

    def test_bad_input(self):
        with self.assertRaises(TypeError):
            self.penalties.set_penalty('a', ['a'])
        with self.assertRaises(TypeError):
            self.penalties.set_penalty(['a'], 'a')
        with self.assertRaises(TypeError):
            self.penalties.set_penalty(['a'], ['a'])
        with self.assertRaises(TypeError):
            self.penalties.set_penalty(None, 'a')
        with self.assertRaises(TypeError):
            self.penalties.set_penalty('a', None)
        with self.assertRaises(TypeError):
            self.penalties.set_penalty(None, None)

        with self.assertRaises(TypeError):
            self.penalties.swap_cost('a', ['a'])
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('a', ['a'])
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('a', ['a'])
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('a', None)
        with self.assertRaises(TypeError):
            self.penalties.swap_cost(None, ['a'])
        with self.assertRaises(TypeError):
            self.penalties.swap_cost(None, None)

    def test_penalty_setting(self):
        old_penalty = self.penalties.get_swap_penalty()
        new_penalty = 7
        new_new_penalty = 102
        self.assertNotEqual(old_penalty, new_penalty)
        self.assertNotEqual(old_penalty, new_new_penalty)

        self.assertEqual(self.penalties.swap_cost('a', 'b'),
                    old_penalty)
        self.assertEqual(self.penalties.swap_cost('b', 'a'),
                    old_penalty)
        self.assertEqual(self.penalties.get_swap_penalty(),
                    old_penalty)

        self.penalties.set_penalty('a', 'b', new_penalty)
        self.assertEqual(self.penalties.swap_cost('a', 'b'),
                    new_penalty)
        self.assertEqual(self.penalties.swap_cost('b', 'a'),
                    old_penalty)
        self.assertEqual(self.penalties.get_swap_penalty(),
                    old_penalty)

        self.penalties.set_penalty('a', 'b', new_new_penalty)
        self.assertEqual(self.penalties.swap_cost('a', 'b'),
                    new_new_penalty)
        self.assertEqual(self.penalties.swap_cost('b', 'a'),
                    old_penalty)
        self.assertEqual(self.penalties.get_swap_penalty(),
                    old_penalty)

class TestErrorGroupPenalties(unittest.TestCase):
    
    def setUp(self):
        self.penalties = fwim.ErrorGroupPenalties()
        
    def test_penalties(self):
        group_penalty = 3
        base = 'e'
        group = 'éèëẽê'
        old_penalty = self.penalties.get_swap_penalty()
        self.assertNotEqual(group_penalty, old_penalty)
        
        self.assertEqual(self.penalties.swap_cost('e', 'é'),
                    old_penalty)
        self.penalties.set_error_group_penalty(base, group, group_penalty)
        self.assertEqual(self.penalties.swap_cost('e', 'é'),
                    group_penalty)
        self.assertEqual(self.penalties.swap_cost('a', 'é'),
                    old_penalty)
        self.assertEqual(self.penalties.swap_cost('é', 'a'),
                    old_penalty)
        self.assertEqual(self.penalties.swap_cost('è', 'e'),
                    group_penalty)
        self.assertEqual(self.penalties.swap_cost('é', 'ë'),
                    group_penalty)
        self.assertEqual(self.penalties.swap_cost('é', 'é'),
                    0)
        self.assertEqual(self.penalties.swap_cost('e', 'e'),
                    0)

class TestAccentAdder(unittest.TestCase):
    
    def setUp(self):
        self.penalties = fwim.ErrorGroupPenalties()
    
    def test_error_groups(self):
        group_penalty = 3
        old_penalty = self.penalties.get_swap_penalty()
        self.assertNotEqual(group_penalty, old_penalty)
        
        self.assertEqual(self.penalties.swap_cost('e', 'é'),
                    old_penalty)
        self.assertEqual(self.penalties.swap_cost('a', 'ä'),
                    old_penalty)
        self.assertEqual(self.penalties.swap_cost('e', 'á'),
                    old_penalty)
        fwim.add_accent_groups(self.penalties, group_penalty)
        self.assertEqual(self.penalties.swap_cost('e', 'é'),
                    group_penalty)
        self.assertEqual(self.penalties.swap_cost('a', 'ä'),
                    group_penalty)
        self.assertEqual(self.penalties.swap_cost('e', 'á'),
                    old_penalty)

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
                         self.penalties.get_end_add_penalty())
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
                         self.penalties.get_end_add_penalty())

class TestEndAddEvaluator(unittest.TestCase):
    
    def setUp(self):
        self.penalties = fwim.LessEndPenalties()
        self.evaluator = fwim.EditDistanceEvaluator(self.penalties)
        
    def test_end_penalties(self):
        self.assertEquals(self.evaluator.distance('hello', 'hello'), 0)
        self.assertEquals(self.evaluator.distance('hello', 'aaahello'),
                        3*self.penalties.get_add_penalty())
        self.assertEquals(self.evaluator.distance('hello', 'haaaello'),
                        3*self.penalties.get_add_penalty())
        self.assertEquals(self.evaluator.distance('hello', 'helloaaa'),
                        3*self.penalties.get_end_add_penalty())

class TestPlainLevenshtein(unittest.TestCase):

    def setUp(self):
        self.penalties = fwim.PlainLevenshteinPenalties()
        self.dev = fwim.EditDistanceEvaluator(self.penalties)

    def test_penalties(self):
        penalty = self.penalties.get_swap_penalty()
        self.assertEqual(penalty, self.dev.distance('fool', 'foot'))
        self.assertEqual(penalty, self.dev.distance('fool', 'tool'))
        self.assertEqual(2*penalty, self.dev.distance('foot', 'tool'))
        self.assertEqual(2*penalty, self.dev.distance('abc', 'bac'))

class TestIgnoreOrderPenalties(unittest.TestCase):
    def setUp(self):
        self.penalties = fwim.IgnoreOrderPenalties()

    def test_bad_input(self):
        with self.assertRaises(TypeError):
            self.penalties.set_penalty('a', ['a'])
        with self.assertRaises(TypeError):
            self.penalties.set_penalty(['a'], 'a')
        with self.assertRaises(TypeError):
            self.penalties.set_penalty(['a'], ['a'])
        with self.assertRaises(TypeError):
            self.penalties.set_penalty(None, 'a')
        with self.assertRaises(TypeError):
            self.penalties.set_penalty('a', None)
        with self.assertRaises(TypeError):
            self.penalties.set_penalty(None, None)

        with self.assertRaises(TypeError):
            self.penalties.swap_cost('a', ['a'])
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('a', ['a'])
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('a', ['a'])
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('a', None)
        with self.assertRaises(TypeError):
            self.penalties.swap_cost(None, ['a'])
        with self.assertRaises(TypeError):
            self.penalties.swap_cost(None, None)

    def test_order(self):
        old_penalty = self.penalties.get_swap_penalty()
        new_penalty = 7
        new_new_penalty = 42
        self.assertNotEqual(old_penalty, new_penalty)

        self.assertEqual(self.penalties.swap_cost('a', 'b'),
                    old_penalty)
        self.assertEqual(self.penalties.swap_cost('b', 'a'),
                    old_penalty)
        self.assertEqual(self.penalties.get_swap_penalty(),
                    old_penalty)

        self.penalties.set_penalty('a', 'b', new_penalty)
        self.assertEqual(self.penalties.swap_cost('a', 'b'),
                    new_penalty)
        self.assertEqual(self.penalties.swap_cost('b', 'a'),
                    new_penalty)
        self.assertEqual(self.penalties.get_swap_penalty(),
                    old_penalty)

        self.penalties.set_penalty('b', 'a', new_new_penalty)
        self.assertEqual(self.penalties.swap_cost('a', 'b'),
                    new_new_penalty)
        self.assertEqual(self.penalties.swap_cost('b', 'a'),
                    new_new_penalty)
        self.assertEqual(self.penalties.get_swap_penalty(),
                    old_penalty)

class TestCaseInsensitiveIgnoreOrderPenalties(unittest.TestCase):
    def setUp(self):
        self.penalties = fwim.CaseInsensitiveIgnoreOrderPenalties()

    def test_bad_input(self):
        with self.assertRaises(TypeError):
            self.penalties.set_penalty('a', ['a'])
        with self.assertRaises(TypeError):
            self.penalties.set_penalty(['a'], 'a')
        with self.assertRaises(TypeError):
            self.penalties.set_penalty(['a'], ['a'])
        with self.assertRaises(TypeError):
            self.penalties.set_penalty(None, 'a')
        with self.assertRaises(TypeError):
            self.penalties.set_penalty('a', None)
        with self.assertRaises(TypeError):
            self.penalties.set_penalty(None, None)

        with self.assertRaises(TypeError):
            self.penalties.swap_cost('a', ['a'])
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('a', ['a'])
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('a', ['a'])
        with self.assertRaises(TypeError):
            self.penalties.swap_cost('a', None)
        with self.assertRaises(TypeError):
            self.penalties.swap_cost(None, ['a'])
        with self.assertRaises(TypeError):
            self.penalties.swap_cost(None, None)

    def test_order(self):
        old_penalty = self.penalties.get_swap_penalty()
        new_penalty = 7
        self.assertNotEqual(old_penalty, new_penalty)

        self.assertEqual(self.penalties.swap_cost('a', 'b'),
                    old_penalty)
        self.assertEqual(self.penalties.swap_cost('b', 'a'),
                    old_penalty)
        self.assertEqual(self.penalties.get_swap_penalty(),
                    old_penalty)

        self.penalties.set_penalty('a', 'b', new_penalty)
        self.assertEqual(self.penalties.swap_cost('a', 'b'),
                    new_penalty)
        self.assertEqual(self.penalties.swap_cost('b', 'a'),
                    new_penalty)
        self.assertEqual(self.penalties.get_swap_penalty(),
                    old_penalty)

    def test_case_insensitivity(self):
        old_penalty = self.penalties.get_swap_penalty()
        new_penalty = 7
        new_new_penalty = 42
        self.assertNotEqual(old_penalty, new_penalty)
        self.assertNotEqual(old_penalty, new_new_penalty)

        self.assertEqual(self.penalties.swap_cost('c', 'd'),
                    old_penalty)
        self.assertEqual(self.penalties.swap_cost('C', 'd'),
                    old_penalty)
        self.assertEqual(self.penalties.swap_cost('c', 'D'),
                    old_penalty)
        self.assertEqual(self.penalties.swap_cost('C', 'D'),
                    old_penalty)

        self.penalties.set_penalty('c', 'd', new_penalty)
        self.assertEqual(self.penalties.swap_cost('c', 'd'),
                    new_penalty)
        self.assertEqual(self.penalties.swap_cost('C', 'd'),
                    new_penalty)
        self.assertEqual(self.penalties.swap_cost('c', 'D'),
                    new_penalty)
        self.assertEqual(self.penalties.swap_cost('C', 'D'),
                    new_penalty)
        self.assertEqual(self.penalties.get_swap_penalty(),
                    old_penalty)

        self.penalties.set_penalty('C', 'D', new_new_penalty)
        self.assertEqual(self.penalties.swap_cost('c', 'd'),
                    new_new_penalty)
        self.assertEqual(self.penalties.swap_cost('C', 'd'),
                    new_new_penalty)
        self.assertEqual(self.penalties.swap_cost('c', 'D'),
                    new_new_penalty)
        self.assertEqual(self.penalties.swap_cost('C', 'D'),
                    new_new_penalty)
        self.assertEqual(self.penalties.get_swap_penalty(),
                    old_penalty)

    def test_case_insensitivity_and_order(self):
        old_penalty = self.penalties.get_swap_penalty()
        new_penalty = 7
        new_new_penalty = 42
        self.assertNotEqual(old_penalty, new_penalty)
        self.assertNotEqual(old_penalty, new_new_penalty)

        self.assertEqual(self.penalties.swap_cost('e', 'f'),
                    old_penalty)
        self.assertEqual(self.penalties.swap_cost('E', 'F'),
                    old_penalty)
        self.assertEqual(self.penalties.swap_cost('f', 'e'),
                    old_penalty)
        self.assertEqual(self.penalties.swap_cost('F', 'E'),
                    old_penalty)

        self.penalties.set_penalty('e', 'f', new_penalty)
        self.assertEqual(self.penalties.swap_cost('e', 'f'),
                    new_penalty)
        self.assertEqual(self.penalties.swap_cost('E', 'F'),
                    new_penalty)
        self.assertEqual(self.penalties.swap_cost('f', 'e'),
                    new_penalty)
        self.assertEqual(self.penalties.swap_cost('F', 'E'),
                    new_penalty)
        
        self.penalties.set_penalty('F', 'E', new_new_penalty)
        self.assertEqual(self.penalties.swap_cost('e', 'f'),
                    new_new_penalty)
        self.assertEqual(self.penalties.swap_cost('E', 'F'),
                    new_new_penalty)
        self.assertEqual(self.penalties.swap_cost('f', 'e'),
                    new_new_penalty)
        self.assertEqual(self.penalties.swap_cost('F', 'E'),
                    new_new_penalty)

class TestBasicWordMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = fwim.BasicWordMatcher()

    def test_bad_input(self):
        with self.assertRaises(TypeError):
            self.matcher.add_word(['a'])
        with self.assertRaises(TypeError):
            self.matcher.add_word(None)
        with self.assertRaises(TypeError):
            self.matcher.add_word('a a')
        with self.assertRaises(TypeError):
            self.matcher.add_word(None, ' a')
        with self.assertRaises(TypeError):
            self.matcher.add_word('a ')

        with self.assertRaises(TypeError):
            self.matcher.find_closest(['a'])
        with self.assertRaises(TypeError):
            self.matcher.find_closest(None)

    def test_matching(self):
        self.matcher.add_word('one')
        self.matcher.add_word('two')
        self.matcher.add_word('three')

        (penalty, match) = self.matcher.find_closest('ane')
        self.assertEqual(match, 'one')
        (penalty, match) = self.matcher.find_closest('to')
        self.assertEqual(match, 'two')
        (penalty, match) = self.matcher.find_closest('thrice')
        self.assertEqual(match, 'three')
        
    def test_matching(self):
        self.matcher.add_word('aaa_aaa')
        self.matcher.add_word('aaa_aab')
        self.matcher.add_word('aaa_abb')
        self.matcher.add_word('aaa_bbb')
        swap_p = self.matcher.get_penalties().get_swap_penalty()
        
        self.assertEqual(len(self.matcher.find_within('aaa_aa', 0)), 0)
        self.assertEqual(len(self.matcher.find_within('aaa_aaa', 0)), 1)
        self.assertEqual(len(self.matcher.find_within('aaa_aaa', swap_p)), 2)
        self.assertEqual(len(self.matcher.find_within('aaa_aaa', 2*swap_p)), 3)
        self.assertEqual(len(self.matcher.find_within('aaa_aaa', 3*swap_p)), 4)
        
    def test_spaces(self):
        m_s = fwim.BasicWordMatcher(allow_spaces=True)
        m_s.add_word("foo bar")

class TestCaseInsensitiveWordMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = fwim.CaseInsensitiveWordMatcher()

    def test_bad_input(self):
        with self.assertRaises(TypeError):
            self.matcher.add_word(['a'])
        with self.assertRaises(TypeError):
            self.matcher.add_word(None)
        with self.assertRaises(TypeError):
            self.matcher.add_word('a a')
        with self.assertRaises(TypeError):
            self.matcher.add_word(None, ' a')
        with self.assertRaises(TypeError):
            self.matcher.add_word('a ')

        with self.assertRaises(TypeError):
            self.matcher.find_closest(['a'])
        with self.assertRaises(TypeError):
            self.matcher.find_closest(None)

    def test_matching(self):
        self.matcher.add_word('one')
        self.matcher.add_word('two')
        self.matcher.add_word('three')

        (penalty, match) = self.matcher.find_closest('ane')
        self.assertEqual(match, 'one')
        (penalty, match) = self.matcher.find_closest('to')
        self.assertEqual(match, 'two')
        (penalty, match) = self.matcher.find_closest('thrice')
        self.assertEqual(match, 'three')

        (penalty, match) = self.matcher.find_closest('ONE')
        self.assertEqual(match, 'one')
        self.assertEqual(penalty, 0)
        (penalty, match) = self.matcher.find_closest('OnE')
        self.assertEqual(match, 'one')
        self.assertEqual(penalty, 0)

        self.matcher.add_word('FOUR')
        (penalty, match) = self.matcher.find_closest('four')
        self.assertEqual(match, 'four')
        self.assertEqual(penalty, 0)
        (penalty, match) = self.matcher.find_closest('fOUr')
        self.assertEqual(match, 'four')
        self.assertEqual(penalty, 0)

class TestBKTree(unittest.TestCase):
    def setUp(self):
        self.penalties = fwim.PlainLevenshteinPenalties()
        self.dev = fwim.EditDistanceEvaluator(self.penalties)
        self.bktree = fwim.BKTree(self.dev)

    def test_matching(self):
        penalty = self.penalties.get_add_penalty()
        self.assertEqual(len(self.bktree.find('helo', 10000)), 0)

        self.bktree.add_word('fool')
        match = self.bktree.find('fool', 0)
        self.assertEqual(len(match), 1)
        self.assertEqual(0, match[0][0])
        self.assertEqual('fool', match[0][1])
        
        self.bktree.add_word('foot')
        match = self.bktree.find('foot', 0)
        self.assertEqual(len(match), 1)
        self.assertEqual(0, match[0][0])
        self.assertEqual('foot', match[0][1])

        match = self.bktree.find('foot', penalty)
        self.assertEqual(len(match), 2)
        self.assertEqual(0, match[0][0])
        self.assertEqual('foot', match[0][1])

        self.bktree.add_word('tool')
        match = self.bktree.find('foot', penalty)
        self.assertEqual(len(match), 2)
        self.assertEqual(0, match[0][0])
        self.assertEqual('foot', match[0][1])

        match = self.bktree.find('foot', 2*penalty)
        self.assertEqual(len(match), 3)
        self.assertEqual(0, match[0][0])
        self.assertEqual('foot', match[0][1])

if __name__ == '__main__':
    unittest.main()
