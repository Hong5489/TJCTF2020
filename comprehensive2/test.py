m = b'the flag is here!  tjctf{aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}'
n = b'abcdefg'

a = b'abcdefghijklmnopqrstuvwxyz'
p = b' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

assert len(m) == 63 and set(m).issubset(set(a + p))
assert len(n) == 7  and set(n).issubset(set(a))
assert m.count(b'tjctf{') == 1 and m.count(b'}') == 1 and m.count(b' ') == 5
text = []
for k in range(0, len(m), 21):
	for j in range (0, 21, 3):
		for i in range(j + k, j + k + 3):
			text.append(m[i] ^ n[j // 3] ^ n[i - j - k] ^ n[k // 21])
print(text)

# print(str([x for z in  for y in z for x in y])[1:-1])