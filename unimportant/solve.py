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