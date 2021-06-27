
import tool
import MDAnalysis
from argparse import ArgumentParser
import multiprocessing
import os
import sys


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument("-trr", "--trajectory", type=str, help="path of trr")
    argparser.add_argument("-pdb", "--protein", type=str, help="path of pdb")
    argparser.add_argument("-prob", "--probtxt", type=str, help="path of pdb")
    argparser.add_argument("-name", "--name_kei", type=str, help="name of file")
    return argparser.parse_args()


def con_thle(name, frm, MED, PROB, result_list):
    u = MDAnalysis.Universe(frm)
    frm = u.trajectory
    print("start:", name, "len TRR:", len(frm), "LEN PROB:", len(PROB))
    MED26 = [0.0 for i5 in range(92)]
    for i in range((int(name)-1) * 1000, (int(name)-1) * 1000 + 1000):
        if float(PROB[i]) > 0:
            cor = frm[i]
            kai = []
            for i1 in range(92):
                for j1 in MED[i1]:
                    num1 = 0
                    for j in range(92, len(MED)):
                        for j2 in MED[j]:
                            a = tool.contact_list(cor[j1],
                                                  cor[j2])
                            if a <= 6.5:
                                num1 += 1
                                break
                            elif a >= 30:
                                break
                        if num1 == 1:
                            break
                    if num1 == 1:
                        break
                kai.append(int(num1))
            # print(cor[j1], cor[j2])]
            for jj in range(len(kai)):
                MED26[jj] = float(MED26[jj]) + float(kai[jj] * PROB[i])
            # print(kai[70:80])
            # print(MED26[70:80])
    # print(aa)
    MED26 = [int(name)] + MED26
    result_list.append(MED26)
    print("end:", name)
    # results[threading.current_thread().name] = MED26


def main():
    thread_list = []
    args = get_option()
    manager = multiprocessing.Manager()
    result_list = manager.list()
    num1 = 1
    num2 = 0
    kai = []
    MED = []
    nun = 0
    for i in open(str(args.protein)):
        f = i.split()
        if int(f[5]) == num1:
            if "CA" == f[2]:
                kai.append(int(f[1]))
        else:
            MED.append(kai)
            if "CA" == f[2]:
                kai = [int(f[1])]
            else:
                kai = []
            num1 += 1
            if f[4] == "B" and num2 == 0:
                num2 += 1
                num1 = 1
    MED.append(kai)
    # print(MED)
    # print(len(MED))
    # sys.exit()
    PROB = []
    for i in open(str(args.probtxt)):
        PROB.append(float(i))
    # print(frm)
    # kai1 = 0.0
    # results = dict()
    u = MDAnalysis.Universe(str(args.trajectory))
    frm = u.trajectory
    NUM = [int(i) for i in range(1, int((len(frm)/1000)) + 1)]
    del frm
    # NUM = [int(i) for i in range(1,15)]
    while True:
        for i in NUM:
            # ifrm = list(frm[(i-1) * 1000:(i-1) * 1000 + 1000])
            # thread = con_thle(i, frm, MED, iPROB, result_list)
            thread = multiprocessing.Process(target=con_thle,
                                             args=(i, str(args.trajectory), MED, PROB, result_list),
                                             name=i)
            thread.start()
            thread_list.append(thread)
            if len(thread_list) == 100:
                for thread in thread_list:
                    thread.join()
                for k in result_list:
                    f = open("TEST2CA/{0}_{1}.txt".format(str(args.name_kei),
                                                       k[0]), "w")
                    for j2 in k:
                        aa = str(j2) + " "
                        f.write(aa)
                    f.write("\n")
                    f.close()
                result_list = manager.list()
                thread_list = []
            """
            elif len(NUM) < 10:
                for thread in thread_list:
                    thread.join()
                for k in result_list:
                    f = open("TEST/{0}_{1}.txt".format(str(args.name_kei),
                                                       k[0]), "w")
                    for j2 in k:
                        aa = str(j2) + " "
                        f.write(aa)
                    f.write("\n")
                result_list = manager.list()
                thread_list = []
            """
        if len(result_list) > 0:
            for thread in thread_list:
                thread.join()
            for k in result_list:
                f = open("TEST2CA/{0}_{1}.txt".format(str(args.name_kei),
                                                   k[0]), "w")
                for j2 in k:
                    aa = str(j2) + " "
                    f.write(aa)
                f.write("\n")
                f.close()
            result_list = manager.list()
            thread_list = []
        testdate = []
        for i in NUM:
            if os.path.exists("TEST2CA/{0}_{1}.txt".format(str(args.name_kei), i)):
                pass
            else:
                testdate.append(i)
        if len(testdate) > 0:
            NUM = testdate
        else:
            break


if __name__ == '__main__':
    main()
