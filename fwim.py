#!/usr/bin/python3 -tt

#    Search for matches in word lists accounting for errors
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

class BasicPenalties():
    """Basic Damerau-Levenshtein distance errors."""

    def __init__(self):
        self.transpose_penalty = 10 # 'ab' -> 'ba'
        self.drop_penalty = 10      # 'abc' -> 'ac'
        self.add_penalty = 10       # 'ac' -> 'abc'
        self.swap_penalty = 10      # 'ab' -> 'ac'

    def get_transpose_penalty(self):
        return self.transpose_penalty

    def get_drop_penalty(self):
        return self.drop_penalty

    def get_add_penalty(self):
        return self.add_penalty

    def get_swap_penalty(self):
        return self.swap_penalty

    def swap_cost(self, character1, character2):
        """The cost of replacing character 1
with character 2. If arguments are not characters,
an exception will be thrown."""
        if type(character1) != type('a'):
            raise TypeError("First argument not a Unicode character.")
        if type(character2) != type('a'):
            raise TypeError("Second argument not a Unicode character.")
        if len(character1) != 1:
            raise TypeError("First argument not a single character.")
        if len(character2) != 1:
            raise TypeError("Second argument not a single character.")
        if character1 == character2:
            return 0
        return self.get_swap_penalty()

class DistinctPenalties(BasicPenalties):
    """A class for testing that has different
values for every type of error."""

    def __init__(self):
        super(DistinctPenalties, self).__init__()
        self.transpose_penalty = 11
        self.drop_penalty = 12
        self.add_penalty = 13
        self.swap_penalty = 14


class EditDistanceEvaluator():
    
    def __init__(self, penalties):
        self.penalties = penalties

    def distance(self, source, target):
        return 15
