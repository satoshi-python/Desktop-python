
from cython import boundscheck, wraparound
from libc.math cimport sqrt, acos
import numpy as np

cdef contact(list x, list y):
  cdef double S = 0
  with boundscheck(False), wraparound(False):
    for i in range(3):
      S += (x[i] - y[i]) ** 2
  return sqrt(S)


def con(list x,list y):
  return contact(x, y)

cdef Angle(list x, list y, list z):
  return degree(x, y, z)

cdef degree(list a, list b, list c):
  cdef double ab  = vspan(a,b)
  cdef double bc  = vspan(b,c)
  cdef double ca  = vspan(c,a)
  print(ab, bc, ca)
  cdef double rad = acos((ab*ab+bc*bc-ca*ca)/(2*ab*bc))
  cdef double PI = 3.1415926535897932
  return 180 * rad / PI


cdef vspan(list a, list b):
  return sqrt(iprod(v3sub(a,b),v3sub(a,b)))

cdef v3sub(list a, list b):
  cdef list c = [0.0] * 3
  for i in range(len(c)):
    c[i] = a[i] - b[i]
  return c

cdef iprod(list a, list b):
  cdef double S = 0
  with boundscheck(False), wraparound(False):
    for i in range(len(a)):
      S += (a[i] * b[i])
  return S


def tool_angle(list x, list y, list z):
  return Angle(x,y,z)
