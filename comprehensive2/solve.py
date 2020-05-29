from z3 import *

m = [BitVec("a%i"%i,8) for i in range(63)]
n = [BitVec("n%i"%i,8) for i in range(7)]
output = [1, 18, 21, 18, 73, 20, 65, 8, 8, 4, 24, 24, 9, 18, 29, 21, 3, 21, 14, 6, 18, 83, 2, 26, 86, 83, 5, 20, 27, 28, 85, 67, 5, 17, 2, 7, 12, 11, 17, 0, 2, 20, 12, 26, 26, 30, 15, 44, 15, 31, 0, 12, 46, 8, 28, 23, 0, 11, 3, 25, 14, 0, 65]

a = 'abcdefghijklmnopqrstuvwxyz'
p = ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
s = Solver()
for i in range(63):
	condition = "Or("
	for c in (a+p):
		condition += "m[%i]==%i," %(i,ord(c)) 
	s.add(eval(condition[:-1]+")"))

for i in range(7):
	condition = "Or("
	for c in (a):
		condition += "n[%i]==%i," %(i,ord(c)) 
	s.add(eval(condition[:-1]+")"))

s.add(z3.Sum([ z3.If(bv == ord(' '), 1, 0) for bv in m ]) == 5)
s.add(z3.Sum([ z3.If(bv == ord('}'), 1, 0) for bv in m ]) == 1)
s.add(z3.Sum([ z3.If(And(m[i] == ord('t'),m[i+1] == ord('j'),m[i+2] == ord('c'),m[i+3] == ord('t'),m[i+4] == ord('f')), 1, 0) for i in range(63-5)]) == 1)

index = 0
for k in range(0, len(m), 21):
	for j in range (0, 21, 3):
		for i in range(j + k, j + k + 3):
			s.add((m[i] ^ n[j // 3] ^ n[i - j - k] ^ n[k // 21]) == output[index])
			index += 1
if s.check() == sat:
	modl = s.model()
	m_result = ""
	for i in range(63):
		m_result += chr(modl[m[i]].as_long())
	print(m_result)