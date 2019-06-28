# -*- coding: utf-8 -*-
import string
import subprocess
import random

def id_generator(letter, size = 9, chars = string.ascii_uppercase):
	if len(letter) != 1 or letter not in chars:
		raise Exception('Expected letter')
	return letter + ''.join(random.choice(chars) for _ in range(size))

def rreplace(s, old, new, occurrence):
	li = s.rsplit(old, occurrence)
	return new.join(li)