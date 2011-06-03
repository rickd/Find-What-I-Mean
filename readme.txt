Find What I mean
by Rick Dangerous


Overview

This library intends to find matches in a list of words when there are
spelling errors.

Take a list of three words:

printf
hello
world.

A search for "hallo" gives no matches in SQL or other systems. But
"hello" is probably what the user meant, so that should be returned.

If the list is this:

héllo
hallo
hullo

Then the search "hello" probably means "héllo" as missing accents are
common.

If the list is this:

hello
hella
hellq

Then the search "hellp" probably means "hello", since o and p are very
close in the keyboard, it is the most probable typo.

And so on and so on.
