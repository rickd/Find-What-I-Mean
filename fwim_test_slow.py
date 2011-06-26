#!/usr/bin/python3 -tt
# -*- coding: UTF-8 -*-

#    All tests that are too slow to run during development
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

class TestBasicWordMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = fwim.BasicWordMatcher()

    def test_big(self):
        words = []
        ifile = open('/usr/share/dict/words')
        for w in ifile:
            w = w.strip()
            if not w.endswith("'s") and len(w) > 2:
                words.append(w)
                if len(words) >= 1000:
                    break
        ifile.close()
        
        for w in words:
            self.matcher.add_word(w)
 
        for w in words[:50]:
            (match, penalty) = self.matcher.find_closest(w)
            self.assertEqual(match, w)
 
if __name__ == '__main__':
    unittest.main()
