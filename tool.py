
import numpy as np
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import pandas as pd
import math
import statistics
import os
import glob
import itertools
import MDAnalysis
import pca_free
import matplotlib.pyplot as plt

# take number of pdb
def pdb_not_H(path):
    RES = []
    for i in open(path, "r"):
        f = i.split()
        if "H" not in f[2]:
            RES.append(int(f[1]))
    return RES


def pdb_Ca(path):
    RES = []
    for i in open(path, "r"):
        f = i.split()
        if f[2] == "CA":
            RES.append(int(f[1]))
    return RES


def pdb_donner(path):
    RES_donner = []
    RES = []
    for i in open(path, "r"):
        f = i.split()
        RES.append(f[2])
    num = 0
    for i in range(len(RES)-1):
        if "S" in RES[i][0] or "O" in RES[i][0] or "N" in RES[i][0]:
            if "H" in RES[i+1][0]:
                RES_donner.append(num)
        num += 1
    return RES_donner


def pdb_accepter(path):
    RES_accepter = []
    for i in open(path, "r"):
        f = i.split()
        if "S" in f[2] or "O" in f[2] or "N" in f[2]:
            RES_accepter.append(int(f[1]))
    return RES_accepter


def pdb__sepa(path, distance = 8):
    A = []
    B = []
    for i in open(path, "r"):
        f = i.split()
        k = []
        num_a = 0
        num_b = 0
        if "CA" == f[2]:
            if f[4] == "A":
                k.append(f[6])
                k.append(f[7])
                k.append(f[8])
                A.append(k)
                num_a += 1
            elif f[4] == "B":
                k.append(f[6])
                k.append(f[7])
                k.append(f[8])
                B.append(k)
                num_b += 1
    con = []
    for i in range(len(A)):
        for j in range(len(B)):
            ll = float(contact_list(A[i], B[j]))
            if ll < int(distance):
                con.append(ll)
            else:
                con.append(0)
    return con

# draw map
def map(contac, savepath):
    # fig = plt.figure()
    print(len(contac))
    for i in range(92):
        for j in range(22):
            if contac[j + i * 22] > 0:
                plt.plot(i+1, j+1, marker=".")
    # plt.set_xlim(1,92)
    # plt.set_ylim(1,22)
    plt.xlim(1, 92)
    plt.ylim(1, 22)
    plt.xlabel("MED26NTD")
    plt.ylabel("LIGAND")
    plt.grid(linewidth=1)
    plt.savefig("{0}.png".format(savepath))

# calculate distance by 6 points of coordinate
def contact(x1, y1, z1, x2, y2, z2):
    ka = float(np.linalg.norm(np.array((float(x1), float(y1), float(z1)),
               dtype=float) - np.array((float(x2), float(y2), float(z2)),
               dtype=float)))
    return ka

# calculate distanceby list
def contact_list(a,b):
    kai = float(math.sqrt(sum([(x -y) **2 for (x,y) in zip(a,b)])))
    return kai

# calculate angle (3:center)
def angle(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    A = np.array((x1-x3, y1-y3, z1-z3), dtype=float)
    B = np.array((x2-x3, y2-y3, z2-z3), dtype=float)
    X = np.inner(A, B)
    s = np.linalg.norm(A)
    t = np.linalg.norm(B)
    return math.degrees(math.acos(X/(s*t)))


# take a number by chain
def sepa(path):
    res1 = []
    res2 = []
    gas = []
    gas1 = []
    num2 = 0
    for i in open(path, "r"):
        f = i.split()
        if num2 == 0:
            r = str(f[4])
            num2 += 1
        if r == str(f[4]):
            res1.append(f[1])
            res2.append(f[2])
        if r != str(f[4]):
            gas1.append(res1)
            gas1.append(res2)
            r = str(f[4])
            res1 = []
            res2 = []
            gas.append(gas1)
            gas1 = []
            res1.append(f[1])
            res2.append(f[2])
    gas1.append(res1)
    gas1.append(res2)
    gas.append(gas1)
    print("number of chain type:",len(gas))
    return gas


# take number of donner
def donner(hai):
    kai = []
    for i in range(len(hai[0])):
        if "S" in hai[1][i][0] or "O" in hai[1][i][0] or "N" in hai[1][i][0]:
            if len(hai[1]) > int(i) + 1:
                if "H" in hai[1][i + 1][0]:
                    kai.append(int(hai[0][i]))
    return kai


# take number of
def donner_cal(hai):
    kai = []
    for i in range(len(hai[0])):
        if "S" in hai[1][i][0] or "O" in hai[1][i][0] or "N" in hai[1][i][0]:
            if len(hai[1]) > int(i) + 1:
                if "H" in hai[1][i + 1][0]:
                    num = 0
                    while True:
                        if "H" in hai[1][i + num + 1][0]:
                            num += 1
                        else:
                            kai.append(num)
                            break
    return kai


# take number of accepter
def accepter(hai):
    kai = []
    for i in range(len(hai[0])):
        if "S" in hai[1][i][0] or "O" in hai[1][i][0] or "N" in hai[1][i][0]:
            kai.append(int(hai[0][i]))
    return kai


# take a number of CA
def CA(hai):
    kai = []
    for i in range(len(hai[0])):
        if hai[1][i] == "CA":
            kai.append(hai[0][i])
    return kai


# draw heat map
def heat_map(path, title, x_label, y_label, hai_niji):
    CM = []
    CM1 = []
    yoko = len(hai_niji)
    tate = len(hai_niji[1])
    for i, j in itertools.product(range(yoko), range(tate)):
        CM.append(hai_niji[i][j])
        CM1.append(hai_niji[i][j])
    MAX = np.amax(np.array(CM))
    # MIN = np.amin(np.array(CM))
    df = pd.DataFrame(hai_niji,
                      index=range(1, int(yoko) + 1),
                      columns=range(1, int(tate) + 1))
    df_mask = (df <= statistics.median(CM1))
    # sns.set(font_size=30)
    ax = sns.heatmap(df, cmap="jet", vmin=statistics.median(CM1), vmax=MAX,
                     mask=df_mask, cbar_kws={'label': str(title)})
    ax.grid()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # plt.figure(figsize=(20,10))
    plt.show()
    plt.savefig("{0}".format(path))
    plt.close()
    return


"""
#Extraction pdb faile
def pdb_file(path,hai):
    new_list = sorted(hai)
    num1 = 0
"""


# find directory
def fail(path, tanshi):
    files = glob.glob("{0}/*.{1}".format(path, tanshi))
    return files


class Calculation_part:
    def __init__(self, niji, trr, prob, List):
        self.niji = niji
        # print(len(niji[0]), len(niji[1]))
        self.syoki = [[0 for i in range(len(niji[0]))]
                      for j in range(len(niji[1]))]
        u = MDAnalysis.Universe(trr)
        self.frm = u.trajectory
        self.prob = []
        if "/" in prob:
            for i in open(prob):
                self.prob.append(float(i))
        else:
            u = float(1)/len(self.frm)
            self.prob = [u] * len(self.frm)
        print(sum(self.prob))
        self.num_list = []
        for i in open(List):
            self.num_list.append(int(i))
        del u

    def cal2(self):
        for i, j in itertools.product(self.niji[0][self.num_a],
                                      self.niji[1][self.num_b]):
            num2 = contact(self.frm[i][0], self.frm[i][1],
                           self.frm[i][2], self.frm[j][0],
                           self.frm[j][1], self.frm[j][2])
            if num2 <= 6.5:
                self.syoki[self.num_b][self.num_a] += float(self.prob[self.num1])
                break
            elif num2 >= 15:
                break
            yield

    def cal1(self):
        for self.num_a, self.num_b in itertools.product(range(len(self.niji[0])
                                                              ),
                                                        range(len(self.niji[1])
                                                              )):
            for kk in self.cal2():
                pass

    def calculation(self):
        if len(self.num_list) > 100000:
            frm_kai = iter(self.frm)
            del self.frm
            self.num1 = 0
            while True:
                if len(self.num_list) == 0:
                    break
                try:
                    self.frm = next(frm_kai)
                    if self.num1 in self.num_list:
                        self.num_list.pop(self.num_list.index(self.num1))
                        self.cal1()
                except StopIteration:
                    break
                self.num1 += 1
                yield
        else:
            a = self.frm
            del self.frm
            for i in self.num_list:
                self.frm = a[i]
                self.num1 = i
                self.cal1()
                yield




class Calculation:
    def __init__(self, niji, trr, prob):
        self.niji = niji
        self.syoki = [[0 for i in range(len(niji[0]))]
                      for j in range(len(niji[1]))]
        u = MDAnalysis.Universe(trr)
        self.frm = u.trajectory
        self.prob = []
        if "/" in prob:
            for i in open(prob):
                self.prob.append(float(i))
        else:
            u = float(1)/len(self.frm)
            self.prob = [u] * len(self.frm)
        del u

    def cal(self):
        for num_a, num_b in itertools.product(range(len(self.niji[0])),
                                              range(len(self.niji[1]))):
            for i, j in itertools.product(self.niji[0][num_a],
                                          self.niji[1][num_b]):
                num2 = contact_list(self.frm[i], self.frm[j])
                if num2 <= 6.5:
                    self.syoki[num_b][num_a] += float(self.prob[self.num1])
                    break
                elif num2 >= 15:
                    break

    def calculation(self):
        frm_kai = iter(self.frm)
        del self.frm
        self.num1 = 0
        while True:
            try:
                self.frm = next(frm_kai)
                if self.prob[self.num1] != 0.0:
                    self.cal()
            except StopIteration:
                break
            self.num1 += 1
            yield


# calculate contact by ALL frame
def MD_ALL_CONTACT1(pdb_path, trr_path, prob_path):
    niji = NOT_H(pdb_path)
    print(len(niji[0]), len(niji[1]))
    kai = Calculation(niji, trr_path, prob_path)
    return kai.syoki


def MD_ALL_CONTACT(pdb_path, trr_path, prob_path):
    niji = NOT_H(pdb_path)
    kai = Calculation(niji, trr_path, prob_path)
    a = len(kai.frm)
    num = 0
    for x in kai.calculation():
        num += 1
        print(num, "/", a)
    return kai.syoki

# calculate contact by specific frame
def MD_LIST_CONTACT(pdb_path, trr_path, prob_path, list_path):
    niji = NOT_H(pdb_path)
    kai = Calculation_part(niji, trr_path, prob_path, list_path)
    a = len(kai.frm)
    num = 0
    for x in kai.calculation():
        num += 1
        # print(num, "/", len(kai.num_list))
    return kai.syoki

# take number of not H in 2 chains
def NOT_H(pdb_path, chain_a="A", chain_b="B"):
    A = []
    B = []
    num1a = 1
    num1b = 1
    num1 = 0
    kai = []
    kk = []
    for i in open(pdb_path, "r"):
        f = i.split()
        if int(f[5]) == int(num1a) and f[4] == chain_a and "H" not in f[2][0]:
            kai.append(int(f[1]))
        elif f[4] == chain_a and "H" not in f[2][0]:
            num1a += 1
            A.append(kai)
            kai = []
            kai.append(int(f[1]))
        elif int(f[5]) == int(num1b) and f[4] == chain_b and "H" not in f[2][0]:
            kai.append(int(f[1]))
        elif f[4] == chain_b and "H" not in f[2][0]:
            num1b += 1
            B.append(kai)
            kai = []
            kai.append(int(f[1]))
        if f[4] == chain_b and f[5] == "1" and num1 == 0:
            A.append(kai)
            kai = []
            num1 += 1
    B.append(kai)
    kk.append(A)
    kk.append(B)
    return kk


# calculate contace by 1 pdb
def CONTACT_PDB(niji,pdb_path):
    za = []
    x1 = []
    for i in open(pdb_path, "r"):
        f = i.split()
        x1.append(float(f[6]))
        x1.append(float(f[7]))
        x1.append(float(f[8]))
        za.append(x1)
        x1 = []
    kk = [[0 for i in range(len(niji[1]))] for j in range(len(niji[0]))]
    num_a = 0
    num_b = 0
    for num_a, num_b in itertools.product(range(len(niji[0])), range(len(niji[1]))):
        for i, j in itertools.product(niji[0][num_a], niji[1][num_b]):
            num2 = contact(za[i][0], za[i][1], za[i][2],
                           za[j][0], za[j][1], za[j][2])
            if num2 <= 8:
                kk[num_a][num_b] += 1
                break
    return kk


# calculate contact (distance <=8) by TRR
def CONTACT_MD(niji, md, prob, LIST=np.arange(0, 1000, 1)):
    kk = [[0 for i in range(len(niji[0]))] for j in range(len(niji[1]))]
    for num, num_a, num_b in itertools.product(range(len(LIST)),
                                               range(len(niji[0])),
                                               range(len(niji[1]))):
        print(num_a, num_b, "   ", num, "/", len(LIST))
        for i, j in itertools.product(niji[0][num_a], niji[1][num_b]):
            num2 = contact_list(md[int(LIST[num])][i], md[int(LIST[num])][j])
            if num2 <= 8:
                kk[num_b][num_a] += float(prob[int(LIST[num])])
                break
            elif num2 >= 15:
                break
    return kk


class HY_Calculation:
    def __init__(self, niji, doner, ac, doner_cal, trr, prob, LIST):
        self.ac = ac
        self.do = doner
        self.niji = niji
        self.HAI = LIST
        self.do_cal = doner_cal
        self.syoki = [[float(0) for i in range(len(niji[0]))] for j in range(len(niji[1]))]
        self.syoki2 =  [[float(0) for i in range(len(niji[0]))] for j in range(len(niji[1]))]
        u = MDAnalysis.Universe(trr)
        self.frm = u.trajectory
        self.prob = []
        if "." in prob:
            for i in open(prob):
                self.prob.append(float(i))
        else:
            u = float(1)/len(self.frm)
            self.prob = [u] * len(self.frm)
        del u, niji, ac, doner, LIST

    def ca1(self):
        for self.num_a, self.num_b in itertools.product(self.niji[0],
                                                        self.niji[1]):
            for self.num1, self.num2 in itertools.product(self.num_a,
                                                          self.num_b):
                # define doner or accepter
                if self.num1 in self.ac[0] and self.num2 in self.ac[1]:
                    # distace
                    if contact_list(self.frm[self.num1],self.frm[self.num2]) <= 3.3:
                        # chain_a is donner
                        if self.num1 in self.do[0]:
                            # angle
                            num_angle = []
                            for ii in range(1, int(self.do_cal[0][self.num_a.index(self.num1)]) +1):
                                num_angle.append(angle(self.frm[self.num1][0], self.frm[self.num1][1],self.frm[self.num1][2],self.frm[self.num2][0],self.frm[self.num2][1],self.frm[self.num2][2],self.frm[self.num1 + ii][0],self.frm[self.num1 + ii][1],self.frm[self.num1 + ii][2]))
                            if len([kkknn for kkknn in num_angle if kkknn >= 120]) > 0:
                                self.syoki[self.niji[1].index(self.num_b)][self.niji[0].index(self.num_a)] += self.prob[self.num_prob]
                                self.syoki2[self.niji[1].index(self.num_b)][self.niji[0].index(self.num_a)] += 1
                                # print("ok  ", self.num1, self.num2)
                                break
                        # chain_b is donner
                        if self.num2 in self.do[1]:
                            # anngle
                            num_angle = []
                            for ii in range(1, int(self.do_cal[1][self.num_b.index(self.num2)]) +1):
                                num_angle.append(angle(self.frm[self.num1][0],self.frm[self.num1][1],self.frm[self.num1][2],self.frm[self.num2][0],self.frm[self.num2][1],self.frm[self.num2][2],self.frm[self.num2 + ii][0],self.frm[self.num2 + ii][1],self.frm[self.num2 + ii][2]))
                            if len([kkknn for kkknn in num_angle if kkknn >= 120]) > 0:
                                self.syoki[self.niji[1].index(self.num_b)][self.niji[0].index(self.num_a)] += self.prob[self.num_prob]
                                self.syoki2[self.niji[1].index(self.num_b)][self.niji[0].index(self.num_a)] += 1
                                # print("ok  ", self.num1, self.num2)
                                break
                    elif contact(self.frm[self.num1][0], self.frm[self.num1][1], self.frm[self.num1][2],self.frm[self.num2][0],self.frm[self.num2][1],self.frm[self.num2][2]) > 15:
                        break
            yield

    def calculation(self):
        if len(self.HAI) > 100000:
            frm_kai = iter(self.frm)
            # print(niji[1])
            del self.frm
            self.num_prob = 0
            while True:
                print(self.num_prob, "/", len(self.prob))
                if max(self.prob) < self.num_prob:
                    break
                try:
                    self.frm = next(frm_kai)
                    if self.num_prob + 1 in self.HAI:
                        if self.prob[self.num_prob] != 0.0:
                            for i in self.ca1():
                                pass
                except StopIteration:
                    break
                """
                if self.num_prob % 10000 == 0:
                    heat_map("aff_HY_ver4.png", "title", "MED26", "aff", self.syoki)
                """
                self.num_prob += 1
        else:
            ALL  = self.frm
            num2 = 1
            for j in self.HAI:
                self.num_prob = j
                self.frm = ALL[j]
                print(num2,"/",len(self.HAI))
                num2 += 1
                for i in self.ca1():
                    pass


# calculate hydrogen bond
def HY_CONTACT(pdb, prob, trr, LIST=[int(i) for i in range(1000000)]):
    PDB = sepa(pdb)
    # print(PDB[0])
    niji = NOT_H(pdb)
    DONER = []
    ACCEPTER = []
    DONER_cal = []
    for i in range(2):
        DONER.append(donner(PDB[i]))
        DONER_cal.append(donner_cal(PDB[i]))
        ACCEPTER.append(accepter(PDB[i]))
    # print(len(DONER[1]))
    # print(len(DONER_cal[1]))
    cal = HY_Calculation(niji, DONER, ACCEPTER, DONER_cal, trr, prob, LIST)
    cal.calculation()
    return cal.syoki,cal.syoki2


def MD_to_pdb_chain(trr, pdb, List, new):
    u = MDAnalysis.Universe(trr)
    frm = u.trajectory
    for list_num in List:
        t = 0
        kai = []
        for num1 in open(pdb, "r"):
            d = num1.split()
            if d[0] == "ATOM" and d[3] != "SOL":
                pdb_num1 = num1.split()
                ligandx = ('{:.3f}'.format((frm[list_num][t][0])))
                ligandy = ('{:.3f}'.format((frm[list_num][t][1])))
                ligandz = ('{:.3f}'.format((frm[list_num][t][2])))
                if len(pdb_num1[6]) < len(ligandx):
                    g = len(ligandx) - len(pdb_num1[6])
                    for j1 in range(g):
                        pdb_num1[6] = " " + pdb_num1[6]
                if len(pdb_num1[6]) > len(ligandx):
                    g = len(pdb_num1[6]) - len(ligandx)
                    for j1 in range(g):
                        ligandx = " " + ligandx
                num1 = num1.replace(str(pdb_num1[6]), ligandx)
                if len(pdb_num1[7]) < len(ligandy):
                    g = len(ligandy) - len(pdb_num1[7])
                    for j1 in range(g):
                        pdb_num1[7] = " " + pdb_num1[7]
                if len(pdb_num1[7]) > len(ligandy):
                    g = len(pdb_num1[7]) - len(ligandy)
                    for j1 in range(g):
                        ligandy = " " + ligandy
                num1 = num1.replace(str(pdb_num1[7]), ligandy)
                if len(pdb_num1[8]) < len(ligandz):
                    g = len(ligandz) - len(pdb_num1[8])
                    for j1 in range(g):
                        pdb_num1[8] = " " + pdb_num1[8]
                if len(pdb_num1[8]) > len(ligandz):
                    g = len(pdb_num1[8]) - len(ligandz)
                    for j1 in range(g):
                        ligandz = " " + ligandz
                num1 = num1.replace(str(pdb_num1[8]), ligandz)
                kai.append(num1)
                t += 1
            elif d[0] == "ATOM" and d[3] == "SOL":
                pdb_num1 = num1.split()
                pdb_num1 = ["*"] + pdb_num1
                ligandx = ('{:.3f}'.format((frm[list_num][t][0])))
                ligandy = ('{:.3f}'.format((frm[list_num][t][1])))
                ligandz = ('{:.3f}'.format((frm[list_num][t][2])))
                if len(pdb_num1[6]) < len(ligandx):
                    g = len(ligandx) - len(pdb_num1[6])
                    for j1 in range(g):
                        pdb_num1[6] = " " + pdb_num1[6]
                if len(pdb_num1[6]) > len(ligandx):
                    g = len(pdb_num1[6]) - len(ligandx)
                    for j1 in range(g):
                        ligandx = " " + ligandx
                num1 = num1.replace(str(pdb_num1[6]), ligandx)
                if len(pdb_num1[7]) < len(ligandy):
                    g = len(ligandy) - len(pdb_num1[7])
                    for j1 in range(g):
                        pdb_num1[7] = " " + pdb_num1[7]
                if len(pdb_num1[7]) > len(ligandy):
                    g = len(pdb_num1[7]) - len(ligandy)
                    for j1 in range(g):
                        ligandy = " " + ligandy
                num1 = num1.replace(str(pdb_num1[7]), ligandy)
                if len(pdb_num1[8]) < len(ligandz):
                    g = len(ligandz) - len(pdb_num1[8])
                    for j1 in range(g):
                        pdb_num1[8] = " " + pdb_num1[8]
                if len(pdb_num1[8]) > len(ligandz):
                    g = len(pdb_num1[8]) - len(ligandz)
                    for j1 in range(g):
                        ligandz = " " + ligandz
                num1 = num1.replace(str(pdb_num1[8]), ligandz)
                num1.pop(int(0))
                kai.append(num1)
                t += 1
        try:
            new_path = new + "pdb_file"
            os.makedirs(new_path)
        except FileExistsError:
            pass
        f = open(new + "pdb_file/frame_{0}.pdb".format(list_num), "w")
        for kai1 in kai:
            f.write(str(kai1))
        f.close()


def MD_to_pdb_not_chain(trr, pdb, List):
    u = MDAnalysis.Universe(trr)
    frm = u.trajectory
    for list_num in List:
        t = 0
        kai = []
        for num1 in open(pdb, "r"):
            d = num1.split()
            if d[0] == "ATOM":
                pdb_num1 = num1.split()
                pdb_num1 = ["*"] + pdb_num1
                ligandx = ('{:.3f}'.format((frm[list_num][t][0])))
                ligandy = ('{:.3f}'.format((frm[list_num][t][1])))
                ligandz = ('{:.3f}'.format((frm[list_num][t][2])))
                if len(pdb_num1[6]) < len(ligandx):
                    g = len(ligandx) - len(pdb_num1[6])
                    for j1 in range(g):
                        pdb_num1[6] = " " + pdb_num1[6]
                if len(pdb_num1[6]) > len(ligandx):
                    g = len(pdb_num1[6]) - len(ligandx)
                    for j1 in range(g):
                        ligandx = " " + ligandx
                num1 = num1.replace(str(pdb_num1[6]), ligandx)
                if len(pdb_num1[7]) < len(ligandy):
                    g = len(ligandy) - len(pdb_num1[7])
                    for j1 in range(g):
                        pdb_num1[7] = " " + pdb_num1[7]
                if len(pdb_num1[7]) > len(ligandy):
                    g = len(pdb_num1[7]) - len(ligandy)
                    for j1 in range(g):
                        ligandy = " " + ligandy
                num1 = num1.replace(str(pdb_num1[7]), ligandy)
                if len(pdb_num1[8]) < len(ligandz):
                    g = len(ligandz) - len(pdb_num1[8])
                    for j1 in range(g):
                        pdb_num1[8] = " " + pdb_num1[8]
                if len(pdb_num1[8]) > len(ligandz):
                    g = len(pdb_num1[8]) - len(ligandz)
                    for j1 in range(g):
                        ligandz = " " + ligandz
                num1 = num1.replace(str(pdb_num1[8]), ligandz)
                # num1.pop(0)
                kai.append(num1)
                t += 1
        try:
            os.makedirs("pdb_file")
        except FileExistsError:
            pass
        f = open("pdb_file/frame_{0}.pdb".format(list_num), "w")
        for kai1 in kai:
            f.write(str(kai1))
        f.close()


class CON_CA:
    def __init__(self, niji, trr, prob):
        self.niji = niji
        self.prob = []
        if "/" in prob:
            for i in open(prob):
                self.prob.append(float(i))
        else:
            u = float(1)/len(self.frm)
            self.prob = [u] * len(self.frm)
        u = MDAnalysis.Universe(trr)
        self.frm = u.trajectory
        self.syoki = [[0 for j in range(len(niji[0]))]
                      for j in range(len(niji[1]))]

    def cal(self):
        frm_kai = iter(self.frm)
        self.num = 0
        while True:
            try:
                self.frm = next(frm_kai)
                if self.prob[self.num] != 0:
                    self.cal1()
            except StopIteration:
                break
            self.num += 1
            yield

    def cal1(self):
        for i, j in itertools.product(self.niji[0], self.niji[1]):
            num1 = contact(self.frm[i][0], self.frm[i][1], self.frm[i][2], self.frm[j][0], self.frm[j][1], self.frm[j][2])
            if num1 < 6.5:
                self.syoki[self.niji[1].index(j)][self.niji[0].index(i)] += self.prob[self.num]


def CONTACT_CA(pdb_path, trr_path, prob_path):
    a = sepa(pdb_path)
    nn = []
    for i in range(len(a)):
        n = []
        for j in range(len(a[i][1])):
            if str(a[i][1][j]) == "CA":
                n.append(int(a[i][0][j]))
        nn.append(n)
    kai = CON_CA(nn, trr_path, prob_path)
    a = len(kai.frm)
    num = 0
    for i in kai.cal():
        num += 1
        print(num, "/", a)
    return kai.syoki


# work flow about pca_free.py
def FREE_FROM_PCA_ALL(a, b, c, d, e):
    txt_path = a
    prob_path = b
    kizami = c
    trr_path = d
    pdb_path = e
    # call class
    a = pca_free.FREE_ENERGY_LANDSCAPE()
    # read file about result of PCA
    for txt in txt_path:
        a.REAS_result_txt(txt)
    # read file about prob
    for prob in prob_path:
        a.CAL1(prob)
    # calculate free energy
    a.CAL2()
    # define kizmai
    a.CAL3(kizami)
    # draw free energy landscape
    a.draw_map()
    # extract pdb files.
    a.pick_up(trr_path, pdb_path)


def FREE_FROM_PCA_EACH(a, b, c, d, e):
    txt_path = a
    A = ["aff", "eaf", "taf", "affkai", "eafkai", "tafkai"]
    prob_path = b
    kizami = c
    trr_path = d
    pdb_path = e
    for i in range(6):
        print(A[i])
        a = pca_free.FREE_ENERGY_LANDSCAPE()
        a.____init__()
        print("ok a.____init__()")
        a.REAS_result_txt(txt_path[i])
        print("ok a.REAS_result_txt(txt_path[i])")
        a.CAL1(prob_path[i])
        print("ok a.CAL1(prob_path[i])")
        a.CAL2()
        print("ok a.CAL2()")
        a.CAL3(kizami)
        print("ok a.CAL3(kizami)")
        a.draw_map(A[i])
        print("ok a.draw_map()")
        # os.mkdir(A[i])
        # a.pick_up(trr_path[i], pdb_path[i], A[i])
        # print("ok a.pick_up(trr_path, pdb_path)")

def yoko_tate(niji,name="yoko_tate.pdf"):
    niji = np.array(niji)
    yoko = np.sum(niji, axis = 0)
    tate = np.sum(niji, axis = 1)
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    plt.subplot(2,1,1)
    plt.plot(np.arange(1,len(yoko)+1), yoko, linewidth=4, color="red")
    plt.title("yoko")
    plt.xlabel("X")
    plt.xticks(np.arange(1,len(yoko)+1,step=5))
    plt.ylabel("Y")
    plt.grid(True)
    plt.subplot(2,1,2)
    plt.plot(np.arange(1,len(tate)+1), tate, linewidth=4, color="red")
    plt.title("yoko")
    plt.xlabel("X")
    plt.xticks(np.arange(1,len(tate)+1,step=3))
    plt.ylabel("Y")
    plt.grid(True)
    del niji,yoko,tate
    plt.savefig(name)


def TRR_TO_PDB(path_trr, path_pdb, list, path=""):
    u = MDAnalysis.Universe(path_pdb, path_trr)
    num = 0
    for i in range(len(u.trajectory)):
        if num == len(list):
            break
        try:
            u.trajectory.next()
            if i + 1 in list:
                num += 1
                ag = u.select_atoms("all")
                if not os.path.exists(path + "pdb_file"):
                    os.mkdir(path + "pdb_file")
                ag.write(path + "pdb_file/{0}.pdb".format(i+1))
        except StopIteration:
            break
