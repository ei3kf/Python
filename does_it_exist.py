## Does whatever is in file one exist in file two?
## If it does, then its a True, if not it's a False.

import sys

a = sys.argv[1]
b = sys.argv[2]

with open(a) as f_a, open(b) as f_b:
    a_lines = set(f_a.read().splitlines())
    b_lines = set(f_b.read().splitlines())
for line in a_lines:
    print(line, '->', line in b_lines)
