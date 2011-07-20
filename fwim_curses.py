#!/usr/bin/python3 -tt
# -*- coding: UTF-8 -*-

#    Query client written in curses.
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


import curses, sys
from fwim import *

stdscr = None

query = ''
matches = []

penalties = LessEndPenalties()
evaluator = EditDistanceEvaluator(penalties)
matcher = BasicWordMatcher(penalties, evaluator)

def load_data(dfile):
    for line in open(dfile):
        matcher.add_word(line.strip())

def init_graphics():
    global stdscr
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)

def draw_screen():
    global stdscr, query
    stdscr.erase()
    stdscr.addstr(0, 0, "Query string (press shift-q to exit)")
    stdscr.addstr(2, 0, query)
    
    for i in range(len(matches)):
        stdscr.addstr(4+i, 0, matches[i][1])
    stdscr.refresh()
    

def shutdown_graphics(foo=None):
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

def process_input():
    global stdscr, query
    c = stdscr.getkey()
    if c == 'Q' or c == 'KEY_ESCAPE':
        sys.exit(0)
    if c == 'KEY_BACKSPACE':
        query = query[:-1]
    else:
        query = (query + c).lower()

def match():
    global query, matches
    if query == '':
        m = []
    else:
        m = matcher.find_within(query, 100)[:10]
    matches = m
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(sys.argv[0] + ' <data file>')
        sys.exit(1)
    load_data(sys.argv[1])
    init_graphics()
    #curses.wrapper(shutdown_graphics)
    draw_screen()
    try:
        while True:
            process_input()
            match()
            draw_screen()
    finally:
        shutdown_graphics()
        print("Query is: " + query)
