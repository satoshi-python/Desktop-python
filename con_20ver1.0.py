

import tool
import MDAnalysis
from argparse import ArgumentParser
import threading


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument("-trr","--trajectory",type=str,help="path of trr")
    argparser.add_argument("-pdb","--protein",type=str,help="path of pdb")
    argparser.add_argument("-prob","--probtxt",type=str,help="path of pdb")
    argparser.add_argument("-name","--name_kei",type=str,help="name of file")
    return argparser.parse_args()


class con_thle(threading.Thread):
    def __init__(self, thread_name, frm, MED, PROB):
        self.frm = frm
        self.prob = PROB
        self.MED = MED
        self.MED26 = [0.0 for i in range(92)]
        self.thread_name = thread_name
        threading.Thread.__init__(self)

    def __str__(self):
        return self.thread_name

    # cal MED 1 residue - ligand 22 residues
    def CAL_LI(self, cor, num):
        num1 = 0
        for j in range(92, 114):
            for j1 in self.MED[j]:
                a = tool.contact_list(cor[num], cor[j1])
                if a <= 6:
                    num1 += 1
                    break
                elif a >= 15:
                    break
            if num1 == 1:
                break
        return num1

    # cal MEd26 92 residues
    def CAL_COR_MED(self, cor):
        kai = []
        for i in range(92):
            for j1 in self.MED[i]:
                jj = self.CAL_LI(cor, j1)
                if jj == 1:
                    break
            kai.append(int(jj))
        return kai

    # thread cal
    def run(self):
        print("start:",self.thread_name,"len TRR:",len(self.frm),"LEN PROB:",len(self.prob))
        for i in range(len(self.frm)):
            if self.prob[i] > 0:
                cor = self.frm[i]
                aa = self.CAL_COR_MED(cor)
                for jj in range(len(aa)):
                    if aa[jj] == 1:
                        self.MED26[jj] += float(self.prob[i])
        print("end:", self.thread_name)

    def get_value(self):
        return self.MED26


# main
def main():
    thread_list = []
    args = get_option()
    num1 = 1
    num2 = 0
    kai = []
    MED = []
    nun = 0
    for i in open(str(args.protein)):
        f = i.split()
        if int(f[5]) == num1:
            if "H" not in f[2]:
                kai.append(int(f[1]))
        else:
            MED.append(kai)
            if "H" not in f[2]:
                kai = [int(f[1])]
            else:
                kai = []
            num1 += 1
            if f[4] == "B" and num2 == 0:
                num2 += 1
                num1 = 1
    MED.append(kai)
    print(MED)
    # print(len(MED))
    PROB = []
    for i in open(str(args.probtxt)):
        PROB.append(float(i))
    u = MDAnalysis.Universe(str(args.trajectory))
    frm = u.trajectory
    # kai1 = 0.0
    for i in range(1, 901):
        thread = con_thle(i, frm[(i-1) * 1000:(i-1) * 1000 + 1000], MED, PROB[(i-1) * 1000:(i-1) * 1000 + 1000])
        # print((i-1) * 1000, ":", (i-1) * 1000 + 1000)
        thread.start()
        thread_list.append(thread)
        if len(thread_list) == 1:
            test=[]
            for thread in thread_list:
                thread.join()
                test.append(thread.get_value())
                nun += 1
                # print(test)
                if nun % 5 == 0 and nun != 0:
                    with open("txt60/{0}_{1}.txt".format(str(args.name_kei), int(nun/5)),"w") as f:
                        for jj in test:
                            for j2 in jj:
                                aa = " " + str(j2)
                                f.write(aa)
                            f.write("\n")
                    test = []
            thread_list = []

if __name__ == '__main__':
    main()
