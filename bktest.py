#!/usr/bin/python3 -tt
# -*- coding: UTF-8 -*-

#    Simple tester for BK tree searcher
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

from fwim import *
import pickle

import sys, time

def load_words():
    ifile = open('/usr/share/dict/words')
    words = []
    for line in ifile:
        w = line.strip()
        if not w.endswith("'s") and len(w) > 2:
            words.append(w)
    return words

def build_bktree(words):
    penalties = PlainLevenshteinPenalties()
    dev = EditDistanceEvaluator(penalties)
    bktree = BKTree(dev)
    
    for w in words:
      bktree.add_word(w)
      
    return bktree

def create_bktree(filename):
    words = load_words()
    buildstart = time.time()
    bktree = build_bktree(words)
    ofile = open(filename, mode='wb')
    pickle.dump(bktree, ofile)
    ofile.close()

def query_bktree(filename):
    bktree = load_bktree(filename)
    searchstart = time.time()
    results = bktree.find('hello', 20)
    searchend = time.time()
    print('Query time: ' + str(searchend-searchstart))

    print(results)

def load_bktree(filename):
    bktree = pickle.load(open(filename, mode='rb'))
    return bktree


if __name__ == '__main__':
    #create_bktree(sys.argv[1])
    query_bktree(sys.argv[1])
