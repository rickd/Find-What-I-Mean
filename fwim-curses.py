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


import curses

stdscr = None

query = ''

def init_graphics():
    global stdscr
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)

def draw_screen():
    global stdscr, query
    stdscr.erase()
    stdscr.addstr(0, 0, "Query string")
    stdscr.addstr(2, 0, query)
    stdscr.refresh()

def shutdown_graphics(foo=None):
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

def process_input():
    global stdscr, query
    c = stdscr.getkey()
    if c == 'KEY_BACKSPACE':
        query = query[:-1]
    if len(c) == '1':
        query += c
    if c == 'KEY_ESCAPE':
        sys.exit(0)

if __name__ == '__main__':
    init_graphics()
    draw_screen()
    try:
        while True:
            process_input()
            draw_screen()
    finally:
        shutdown_graphics()
