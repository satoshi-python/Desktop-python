
import tool
import MDAnalysis
from argparse import ArgumentParser
import multiprocessing
import os


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument("-trr", "--trajectory", type=str, help="path of trr")
    argparser.add_argument("-pdb", "--protein", type=str, help="path of pdb")
    argparser.add_argument("-prob", "--probtxt", type=str, help="path of pdb")
    argparser.add_argument("-name", "--name_kei", type=str, help="name of file")
    return argparser.parse_args()


def con_thle(name, niji, do, ac, do_cal, frm, PROB, result_list):
    u = MDAnalysis.Universe(frm)
    frm = u.trajectory
    print("start:", name, "len TRR:", len(frm), "LEN PROB:", len(PROB))
    MED26 = [0.0 for i in range(92)]
    for (i, ii) in zip(range(len(PROB)), range((name-1) * 1000, (name-1) * 1000 + 1000)):
        if PROB[i] > 0:
            cor = frm[ii]
            kai = []
            # MED26
            for num_a in niji[0]:
                num_MED = 0
                for num1 in num_a:
                    # ligand
                    num_MED = 0
                    for num_b in niji[1]:
                        for num2 in num_b:
                            if num1 in ac[0] and num2 in ac[1]:
                                if tool.contact_list(cor[num1], cor[num2]) <= 3.3:
                                    if num1 in do[0]:
                                        num_angle = []
                                        for iii in range(1, int(do_cal[0][num_a.index(num1)]) +1):
                                            num_angle.append(tool.angle(cor[num1][0], cor[num1][1],cor[num1][2],cor[num2][0],cor[num2][1],cor[num2][2],cor[num1 + iii][0],cor[num1 + iii][1],cor[num1 + iii][2]))
                                        if len([kkknn for kkknn in num_angle if kkknn >= 120]) > 0:
                                            num_MED += 1
                                            break
                                    if num2 in do[1]:
                                        num_angle = []
                                        for iii in range(1, int(do_cal[1][num_b.index(num2)]) +1):
                                            num_angle.append(tool.angle(cor[num1][0],cor[num1][1],cor[num1][2],cor[num2][0],cor[num2][1],cor[num2][2],cor[num2 + iii][0],cor[num2 + iii][1],cor[num2 + iii][2]))
                                        if len([kkknn for kkknn in num_angle if kkknn >= 120]) > 0:
                                            num_MED += 1
                                            break
                        if num_MED == 1:
                            break
                    if num_MED == 1:
                        break
                kai.append(int(num_MED))
            for jj in range(len(kai)):
                if kai[jj] == 1:
                    MED26[jj] += float(PROB[i])
    MED26 = [int(name)] + MED26
    result_list.append(MED26)
    print("end:", name)


def main():
    thread_list = []
    args = get_option()
    manager = multiprocessing.Manager()
    result_list = manager.list()
    PDB = tool.sepa(str(args.protein))
    niji = tool.NOT_H(str(args.protein))
    DONER = []
    ACCEPTER = []
    DONER_cal = []
    for i in range(2):
        DONER.append(tool.donner(PDB[i]))
        DONER_cal.append(tool.donner_cal(PDB[i]))
        ACCEPTER.append(tool.accepter(PDB[i]))
    u = MDAnalysis.Universe(str(args.trajectory))
    frm = u.trajectory
    NUM = [int(i) for i in range(1, int((len(frm)/1000)) + 1)]
    PROB = []
    for i in open(str(args.probtxt)):
        PROB.append(float(i))
    del frm
    while True:
        for i in NUM:
            iPROB = PROB[(i-1) * 1000:(i-1) * 1000 + 1000]
            print((i-1) * 1000, ":", (i-1) * 1000 + 1000)
            thread = multiprocessing.Process(target=con_thle,
                                             args=(i, niji, DONER, ACCEPTER, DONER_cal, str(args.trajectory), iPROB, result_list),
                                             name=i)
            thread.start()
            thread_list.append(thread)
            if len(thread_list) == 100:
                for thread in thread_list:
                    thread.join()
                for k in result_list:
                    f = open("TESTHY/{0}_{1}.txt".format(str(args.name_kei),
                                                       k[0]), "w")
                    for j2 in k:
                        aa = str(j2) + " "
                        f.write(aa)
                    f.write("\n")
                    f.close()
                result_list = manager.list()
                thread_list = []
        if len(result_list) > 0:
            for thread in thread_list:
                thread.join()
            for k in result_list:
                f = open("TESTHY/{0}_{1}.txt".format(str(args.name_kei),
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
            if os.path.exists("TESTHY/{0}_{1}.txt".format(str(args.name_kei), i)):
                pass
            else:
                testdate.append(i)
        if len(testdate) > 0:
            NUM = testdate
        else:
            break


if __name__ == '__main__':
    main()
