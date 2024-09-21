#!/usr/bin/env python3
from random import randint, choice

def get_fixed():
	if randint(1,6) == 1:
		return "you mean we're not going to the park?"
		return choice([
			"you mean we're not going to the park?"
			])

	s = ''
	r = randint(0,2)
	if r == 0:
		n = 'n'
		o = 'o'
	elif r == 1:
		n = ''
		o = 'no'
	if r != 2:
		s += n + o * randint(4,10)

	s += ' ' + choice(['', '*whimpers*', '*whines*'])
	s = s.strip()

	if not s: s = "you mean we're not going to the park?"
	return s

if __name__ == '__main__':
	print(get_fixed())
