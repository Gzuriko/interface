import subprocess
import os

p = subprocess.Popen('ipconfig /all',shell=True,stdout=subprocess.PIPE)

c='Имя компьютера'
c=c.encode('cp866')
for line in p.stdout.readlines():
    if c in line:
        print('PC name ',line.decode('cp866')[39:55])
        print(type(line))
    if b'IPv4' in line:
        print('IP ',line.decode('cp866')[39:52]) 
