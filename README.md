# cart2frac
This script takes lattice vectors, obtains the matrix of the transformation and performs the transform from cartesian to fractional coords. It then proceeds to write them in .gen format that is usable by dftb+. It currently has one dependency : xyz2gen from dptools. This is to ensure that there is not error in formatting. This will eventually be changed.

#xyz2posdirect
Takes a cartesian xyz file to a poscar file in direct coordinates 
