# Comprehensive 2 65 points 
>Reversing - Solved (66 solves)

>Written by boomo

>His power level increased... What do I do now??

>[comprehensive2.py](comprehensive2.py)

>Output: [1, 18, 21, 18, 73, 20, 65, 8, 8, 4, 24, 24, 9, 18, 29, 21, 3, 21, 14, 6, 18, 83, 2, 26, 86, 83, 5, 20, 27, 28, 85, 67, 5, 17, 2, 7, 12, 11, 17, 0, 2, 20, 12, 26, 26, 30, 15, 44, 15, 31, 0, 12, 46, 8, 28, 23, 0, 11, 3, 25, 14, 0, 65]

It got a Python script and the program output

Lets analyze the script:
```py
# m is unknown string
m = '[?????]'
# n also unknown string
n = '[?????]'
# a is all lowercase alphabert
a = 'abcdefghijklmnopqrstuvwxyz'
# p is all punctuation character
p = ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
# the length of m must equal 63
assert len(m) == 63 
# m only contain characters from a and p
assert set(m).issubset(set(a + p))
# the length of n must equal 7
assert len(n) == 7 
# n only contain characters from a
assert set(n).issubset(set(a))
# m only contain one "tjctf{" string
assert m.count('tjctf{') == 1 
# m only contain one "}" string
assert m.count('}') == 1 
# m contain 5 space character
assert m.count(' ') == 5
```

Under all these condition, `m` and `n` will scramble with some calculation then become output:
```py
# The logic is same as the original code
text = []
for k in range(0, 63, 21):
	for j in range (0, 21, 3):
		for i in range(j + k, j + k + 3):
			text.append(m[i] ^ n[j // 3] ^ n[i - j - k] ^ n[k // 21])
print(text)
# [1, 18, ..., 65]
```

Seems like a **z3 problem (SAT solver)**

z3 is normally used for Reversing Challenge to calculate the possible input based on the calculation and output 

## Condition of m
- m is length of 63
- m contains lowercase letter or punctuation
- m contain the flag format (tjctf{}) 
- m contain 5 spaces (" ")

## Condition of n
- n is length of 7
- n contains only lowercase letter

We can guess the m and n will be something like:
```py
m = 'the flag is here!  tjctf{aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}'
n = 'abcdefg'
```

Based on the condition above, we can use z3 to calculate the possible input:
```py
from z3 import *
# Declare m and n as BitVector
m = [BitVec("a%i"%i,8) for i in range(63)]
n = [BitVec("n%i"%i,8) for i in range(7)]
output = [1, 18, ..., 65]

a = 'abcdefghijklmnopqrstuvwxyz'
p = ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
s = Solver()
# Add condition that m is in a and p only
for i in range(63):
	condition = "Or("
	for c in (a+p):
		condition += "m[%i]==%i," %(i,ord(c)) 
	s.add(eval(condition[:-1]+")"))

# Add condition that n is in a only
for i in range(7):
	condition = "Or("
	for c in (a):
		condition += "n[%i]==%i," %(i,ord(c)) 
	s.add(eval(condition[:-1]+")"))

# Add condition that m contain 5 spaces
s.add(z3.Sum([ z3.If(bv == ord(' '), 1, 0) for bv in m ]) == 5)

# Add condition that m contain the flag format tjctf{}
# In range(63-5) because tjctf{ must be together
s.add(z3.Sum([ z3.If(And(m[i] == ord('t'),m[i+1] == ord('j'),m[i+2] == ord('c'),m[i+3] == ord('t'),m[i+4] == ord('f')), 1, 0) for i in range(63-5)]) == 1)
# Add condition that m contain one }
s.add(z3.Sum([ z3.If(bv == ord('}'), 1, 0) for bv in m ]) == 1)
```
After we add the conditions, we can add the calculation for produce the output:
```py
index = 0
for k in range(0, len(m), 21):
	for j in range (0, 21, 3):
		for i in range(j + k, j + k + 3):
			# Add condition that this calculation must equal the output
			s.add((m[i] ^ n[j // 3] ^ n[i - j - k] ^ n[k // 21]) == output[index])
			index += 1
```
Then finally, check is it solvable, print out the flag!
```py
if s.check() == sat:
	modl = s.model()
	m_result = ""
	for i in range(63):
		m_result += chr(modl[m[i]].as_long())
	print(m_result)
```
Result:
```
hata o sagashiteimasu ka? dozo, tjctf{sumimasen_flag_kudasaii}.
```

[Full python script](solve.py)

My z3 script is refer from a [DawgCTF2020 challenge writeup](https://github.com/toomanybananas/dawgctf-2020-writeups/tree/master/reversing/potentially-eazzzy)

## Flag
```
tjctf{sumimasen_flag_kudasaii}
```