#!/usr/bin/env python3


import numpy as np
import sys
import os

def theta(vec1,vec2):
	return np.arccos(float(np.dot(vec1,vec2))/float((np.linalg.norm(vec1)*np.linalg.norm(vec2))))
#lattice vectors
lvax = [ 100., 0., 0.]
lvay = [ 0.,100.,0.]
lvaz = [0.,0.,51.5369]

crd = []
crd2 = []
cart = []
frac = []
atoms = []
# angles and magnitudes
ax = np.linalg.norm(lvax)
ay = np.linalg.norm(lvay)
az = np.linalg.norm(lvaz)
alpha = theta(lvay,lvaz)
beta = theta(lvax,lvaz)
gamma = theta(lvax,lvay)

print(ax, ay, az, alpha, beta, gamma)

v = np.sqrt(1. - (np.cos(alpha))**2. - (np.cos(beta))**2. + (np.cos(gamma))**2. + 2.*np.cos(alpha)*np.cos(beta)*np.cos(gamma))


print(v)
#transformation matrix

T = np.matrix ( [[1./ax, -(np.cos(gamma)/(ax*np.sin(gamma))), ((np.cos(alpha)*np.cos(gamma) - np.cos(beta))/(ax*v*np.sin(gamma)))],[0., 1./(ay*np.sin(gamma)), (np.cos(beta)*np.cos(gamma) - np.cos(alpha))/(ay*v*np.sin(gamma))],[0.,0.,np.sin(gamma)/(az*v)]])

print(T)

file = open(sys.argv[1],'r')

for line in  file:
	k = line.split()
	crd.append(k)

file.close()

for i in range(2,len(crd)):
	crd2.append(np.array([float(crd[i][1]),float(crd[i][2]),float(crd[i][3])]))
	if i%2 == 0:
		atoms.append('B')
	else:
		atoms.append('N')


cart = np.reshape(crd2, (len(crd2),3))

frac =np.array(cart * T)
#print(isinstance(float(crd[2][0]), float))
#print(cart)
#print(frac)
#print(crd[0])

suplist = zip(atoms,frac)

with open('%s.frac' %str(sys.argv[1]),'w') as wf:
    wf.write('%s\n'%(crd[0]))
    wf.write('%s\n'%(crd[1]))
    for row in suplist:
        wf.write('%s \n' %' '.join(map(str,row)))

os.system('sed -e "s/[]]//" -e "s/[[]//" %s.frac > temp'%str(sys.argv[1]))
os.system('mv temp %s.frac'%str(sys.argv[1]))

os.system('sed -i "s/\'//g" %s.frac > temp'%str(sys.argv[1]))
#os.system('mv temp %s.frac'%str(sys.argv[1]))

os.system('sed -i "s/,//g" %s.frac'%str(sys.argv[1]))
#os.system('mv temp %s.frac'%str(sys.argv[1]))

os.system('sed -i "s/e/E/g" %s.frac'%str(sys.argv[1]))

#using xyz2gen from dptools (supplied by dftb-plus.org) until I figure out how to format the output properly in the genfromxyz script 
os.system('xyz2gen %s.frac'%str(sys.argv[1]))
os.system('sed -i "s/C/F/" %s.frac.gen'%str(sys.argv[1]))

u = np.zeros(3)

with open('%s.frac.gen' %str(sys.argv[1]),'a') as writef:
    writef.write("%s \n" %' '.join(map(str, u )))
    writef.write("%s \n" %' '.join(map(str,lvax)))
    writef.write("%s \n" %' '.join(map(str,lvay)))
    writef.write("%s \n" %' '.join(map(str,lvaz)))
