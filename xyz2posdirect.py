#!/usr/bin/env python3


import numpy as np
import os

def theta(vec1,vec2):
	return np.arccos(float(np.dot(vec1,vec2))/float((np.linalg.norm(vec1)*np.linalg.norm(vec2))))

#lattice vectors
lvax = [ 30., 0., 0.]
lvay = [ 0.,30.,0.]
lvaz = [0.,0.,20.036363601685]

crd = []
crd2 = []
cart = []
frac = []

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

file = open("bnnt_forposcar.xyz",'r')

for line in  file:
	k = line.split()
	crd.append(k)

file.close()

for i in range(2,len(crd)):
	crd2.append(np.array([float(crd[i][1]),float(crd[i][2]),float(crd[i][3])]))

cart = np.reshape(crd2, (len(crd2),3))

frac =np.array( cart * T )
#print(isinstance(float(crd[2][0]), float))
print(cart)
print(frac)
print(lvax)
print(frac[0])

os.system('touch boron.posdirect')

with open('boron.posdirect','a') as wfile:
	wfile.write("System BN\n") 
	wfile.write("%s \n" %str(v))
	wfile.write("%s \n" %' '.join(map(str,lvax)))
	wfile.write("%s \n" %' '.join(map(str,lvay)))
	wfile.write("%s \n" %' '.join(map(str,lvaz)))
	wfile.write("80 80 \n")
	wfile.write("Direct \n")
	for row in frac:
		wfile.write("%s \n"%' '.join(map(str, row)))	
