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

    def check_params_single_characters(self, character1, character2):
        if type(character1) != type('s'):
            raise TypeError('Source is not a string.')
        if type(character2) != type('s'):
            raise TypeError('Target is not a string.')
        if len(character1) != 1:
            raise TypeError("First argument not a single character.")
        if len(character2) != 1:
            raise TypeError("Second argument not a single character.")

    def swap_cost(self, character1, character2):
        """The cost of replacing character 1
with character 2. If arguments are not characters,
an exception will be thrown."""
        self.check_params_single_characters(character1, character2)

        if character1 == character2:
            return 0
        return self.get_swap_penalty()

class PlainLevenshteinPenalties(BasicPenalties):
    """A set where the transposition penalty is so
large that it is never chosen."""

    def __init__(self):
        super(PlainLevenshteinPenalties, self).__init__()
        self.transpose_penalty = 100000
        self.drop_penalty = 10
        self.add_penalty = 10
        self.swap_penalty = 10

class DistinctPenalties(BasicPenalties):
    """A class for testing that has different
values for every type of error."""

    def __init__(self):
        super(DistinctPenalties, self).__init__()
        self.transpose_penalty = 11
        self.drop_penalty = 12
        self.add_penalty = 13
        self.swap_penalty = 14

class CustomSwapPenalties(BasicPenalties):
    """A class that allows the user to
    set a custom penalty value for certain
    letter pairs."""

    def __init__(self):
        super(CustomSwapPenalties, self).__init__()
        self.penalties = {}

    def set_penalty(self, character1, character2, penalty_value):
        self.check_params_single_characters(character1, character2)
        self.penalties[(character1, character2)] = penalty_value

    def swap_cost(self, character1, character2):
        self.check_params_single_characters(character1, character2)
        key = (character1, character2)
        if key in self.penalties:
            return self.penalties[key]
        return super(CustomSwapPenalties, self).swap_cost(character1, character2)

class CaseInsensitiveIgnoreOrderPenalties(CustomSwapPenalties):

    def __init__(self):
        super(CaseInsensitiveIgnoreOrderPenalties, self).__init__()

    def order_and_lower(self, character1, character2):
        self.check_params_single_characters(character1, character2)
        character1 = character1.lower()
        character2 = character2.lower()
        if character2 < character1:
            (character1, character2) = (character2, character1)
        return (character1, character2)
    
    def set_penalty(self, character1, character2, penalty_value):
        (character1, character2) = self.order_and_lower(character1, character2)
        super(CaseInsensitiveIgnoreOrderPenalties, self).set_penalty(character1, character2, penalty_value)
        
    def swap_cost(self, character1, character2):
        (character1, character2) = self.order_and_lower(character1, character2)
        return super(CaseInsensitiveIgnoreOrderPenalties, self).swap_cost(character1, character2)
    


class EditDistanceEvaluator():
    
    def __init__(self, penalties):
        self.penalties = penalties

    def distance(self, source, target):
        if type(source) != type('s'):
            raise TypeError('Source is not a string.')
        if type(target) != type('s'):
            raise TypeError('Target is not a string.')

        if len(source) == 0:
            return self.penalties.get_add_penalty()*len(target)
        if len(target) == 0:
            return self.penalties.get_drop_penalty()*len(source)

        return self.__distance(source, target)

    def __distance(self, source, target):
        l1 = len(source)
        l2 = len(target)
        d = []
        for i in range(l1+1):
            d.append([0]*(l2+1))
        
        for i in range(l1+1):
            d[i][0] = i*self.penalties.get_drop_penalty()
        for j in range(l2+1):
            d[0][j] = j*self.penalties.get_add_penalty()

        for j in range(1, l2+1):
            for i in range(1, l1+1):
                source_loc = i-1
                target_loc = j-1
                source_letter = source[source_loc]
                target_letter = target[target_loc]
                subst_penalty = d[i-1][j-1] + \
                    self.penalties.swap_cost(source_letter, target_letter)
                del_penalty = d[i-1][j] + self.penalties.get_drop_penalty()
                add_penalty = d[i][j-1] + self.penalties.get_add_penalty()
                # Transpose is tricky.
                if i >= 2 and j >= 2 and source[source_loc] == target[target_loc-1] and \
                        source[source_loc-1] == target[target_loc]:
                    transpose_penalty = d[i-2][j-2] + self.penalties.get_transpose_penalty()
                else:
                    transpose_penalty = del_penalty + 1 # Ensures this won't be chosen.
                total_penalty = min(subst_penalty, del_penalty,\
                                        add_penalty, transpose_penalty)
                d[i][j] = total_penalty

        return d[-1][-1]

class BasicWordMatcher():
    def __init__(self):
        self.penalties = BasicPenalties()
        self.dev = EditDistanceEvaluator(self.penalties)
        self.words = set()
        
    def size(self):
        return len(self.words)

    def check_string(self, word):
        if type(word) != type('s'):
            raise TypeError('Argument is not a string.')

    def check_single_word(self, word):
        self.check_string(word)
        if ' ' in word:
            raise TypeError('Argument is not a single word.')

    def add_word(self, word):
        self.check_single_word(word)
        self.words.add(word)

    def find_closest(self, word):
        self.check_string(word)
        
        if len(self.words) == 0:
            return ('', self.dev.distance(word, ''))

        min_penalty = 1000000000000
        closest = ''

        for w in self.words:
            dist = self.dev.distance(word, w)
            if dist < min_penalty:
                min_penalty = dist
                closest = w

        return (closest, min_penalty)


# Classic Burkhard-Keller Tree. Note that this only works
# on metrics. Damerau-Levenshtein is _not_ a metric. Plain
# Levenshtein is.

class BKTree():

    def __init__(self, distance_function):
        self.distance = distance_function
        self.root = None

    def add_word(self, word):
        if self.root is None:
            self.root = BKNode(word)
            return
        current = self.root
        self.__add_recursively(current, word)

    def __add_recursively(self, node, word):
        distance = self.distance(word, node.word)
        if distance in node.children:
            self.__add_recursively(node.children[distance], word)
        new_node = BKNode(word)
        node.children[distance] = new_node

    def get_sorted_matches_within(self, query, max_error):
        if self.root is None:
            return []
        matches = []
        self.__match_recursively(self.root, query, max_error, matches)
        return matches

    def __match_recursively(self, node, query, max_error, matches):
        distance = self.distance(word, node.word)
        if distance <= max_error:
            matches.append((distance, node.word))
        for d in node.children.keys():
            if d >= distance-max_error and d <= distance+max_error:
                self.__match_recursively(node.children[d], query, max_error, matches)

class BKNode():
    def __init__(self, word):
        self.word = word
        self.children = {}

