
import numpy as np
import MDAnalysis as MDA
import glob

class Calculation:
    def __init__(self, prob, length, num):
        if prob == "ll":
            self.prob = [float(1/length)] * length
        else:
            self.prob = []
            for i in open(prob):
                self.prob.append(float(i))
        self.answer = [0.0] * len(num[0])
        for i in range(1,len(num)):
            self.answer.append([0.0] * len(num[i]))
    



def READ_TRR(path):
    u = MDA.Universe(path)
    retun u.trajectory

def READ_PDB_select(path, atom):
    test = []
    num = 0
    chain = [chr(ord("A")+i) for i in range(26)]
    kai = []
    for i in open(path):
        f = i.split()
        if f[2] in atom:
            if chain.index(f[4]) - num == 0:
                kai.append(int(f[1]) -1)
            else:
                num = chain.index(f[4])
                test.append(kai)
                kai = []
                kai.append(int(f[1]) -1)
    test.append(kai)
    return test

def READ_PDB_hevy(path):
    test = []
    num = 0
    chain = [chr(ord("A")+i) for i in range(26)]
    kai = []
    for i in open(path):
        f = i.split()
        if "H" not in f[2]:
            if chain.index(f[4]) - num == 0:
                kai.append(int(f[1]) -1)
            else:
                num = chain.index(f[4])
                test.append(kai)
                kai = []
                kai.append(int(f[1]) -1)
    test.append(kai)
    return test

def CON(trr_path, pdb_path, prob = "ll", Threshold_con = 8, Threshold_prob = 0.0, ATOM = "ALL"):
    if "*" in trr_path:
        trr_path = glob.glob(trr_path[:-1]+"*.trr")
    t = READ_TRR(trr_path)
    if ATOM == ALL:
        num = READ_PDB_hevy(pdb_path)
    else:
        num = READ_PDB_select(pdb_path, ATOM)
    CAL = Calculation(prob, len(t), num)
