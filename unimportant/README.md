# Unimportant 60 points
>Forensics - Solved (100 solves)

>Written by KyleForkBomb

>It's probably at least a *bit* important? Like maybe not the least significant, but still unimportant...

[unimportant.png](unimportant.png)

[source](encode.py)

A python script and a PNG picture

Look though the script, it just put the flag in the **second bit of green channel** of the `unimportant.png`

```py
pixel = (pixel[0],                     Red
         pixel[1]&~0b10|(bits[i]<<1),  Green
         pixel[2],                     Blue
         pixel[3])                     Alpha
```
Wrote a [python script](solve.py) to extract the flag:
```py
from PIL import Image
from Crypto.Util.number import long_to_bytes
import re
img = Image.open('unimportant.png')
pixels = img.load()
w,h = img.size
def findFlag():
	flag = 0
	for i in range(w):
		for j in range(h):
			flag |= (pixels[i,j][1] & 0b10)>>1
			flag <<= 1
			if re.findall("tjctf{.*}",long_to_bytes(flag)):
				print(long_to_bytes(flag))
				return
findFlag()
```
## Flag
```
tjctf{n0t_th3_le4st_si9n1fic4nt}
```