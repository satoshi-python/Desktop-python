from argparse import ArgumentParser
import os
import random
import tool
import multiprocessing
MM = "/home/biostr1/SOTU18/got"
TRR_path = [MM + "/med26_aff4/trr/test_all.trr", MM + "/med26_eaf1/trr/test_all.trr", MM + "/med26_taf7/run/test_all.trr",
            MM + "/Med26_aff4_kai/trr/run_all.trr", MM + "/Med26_eaf1_kai/trr/run_all.trr", MM + "/Med26_taf7_kai/trr/run_all.trr"]
pdb_path = [MM + "/med26_aff4/pdb/HEN.pdb", MM + "/med26_eaf1/pdb/HEN.pdb", MM + "/med26_taf7/pdb/HEN_msm.pdb",
            MM + "/Med26_aff4_kai/aff4kai.pdb", MM + "/Med26_eaf1_kai/eaf1kai.pdb", MM + "/Med26_taf7_kai/taf7kai.pdb"]


def PROB():
    MM = "/home/biostr1/SOTU18/got"
    path = [MM + "/med26_aff4/trr/prob.txt", MM + "/med26_eaf1/trr/prob.txt", MM + "/med26_taf7/run/prob.txt",
                MM + "/Med26_aff4_kai/trr/prob.dat", MM + "/Med26_eaf1_kai/trr/prob.dat", MM + "/Med26_taf7_kai/trr/prob.dat"]
    prob = {}
    kai = []
    REB = {}
    for name in path:
        for (t, num) in zip(open(name), range(1, 1000001)):
            if float(t) >= 10 ** -10:
                prob[num] = float(t)
        print(name[31:-13])
        REB[name[31:-13]] = len(prob)
        kai.append(prob)
        prob = {}
    kai.append(REB)
    return kai


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument("-txt", "--cluster", type=str, help="name of file")
    return argparser.parse_args()


def cal_multi(kai, prob, i, new_path, num, result_list):
    name = ["aff4.txt", "eaf.txt", "taf.txt",
            "affkai.txt", "eafkai.txt", "tafkai.txt"]
    test = [[]for i in range(6)]
    num1 = 0
    S_list = []
    for j in kai:
        S = 0
        for (l, key, val) in zip(j, prob[num1].keys(), prob[num1].values()):
            if l == i:
                test[num1].append(int(key))
                S += float(val)
        num1 += 1
        S_list.append(S)
        S = 0
    new_path2 = new_path + "/" + str(i) + "_" + str(sum(S_list))+"/"
    if not os.path.exists(new_path2):
        os.mkdir(new_path2)
    for j in range(6):
        if i != min(num) and  len(test[j]) > 10:
            f = open(new_path2 + str(S_list[j]) + "_" + name[j],"w")
            for j1 in test[j]:
                f.write(str(j1))
                f.write("\n")
            f.close()
            new_path3 = new_path2 + "/" + str(name[j][:-4]) + "/"
            if not os.path.exists(new_path3):
                os.mkdir(new_path3)
            tool.TRR_TO_PDB(TRR_path[j], pdb_path[j], random.sample(test[j], 10), new_path3)
    result_list.append(S_list)
    print("end:", i)


def main():
    prob = PROB()
    args = get_option()
    date = []
    print(str(args.cluster))
    for i in open(str(args.cluster)):
        date.append(int(i))
    num = list(set(date))
    kai = []
    manager = multiprocessing.Manager()
    result_list = manager.list()
    num3 = 0
    kai.append(date[num3:num3 + prob[6]["aff4"]])
    num3 += prob[6]["aff4"]
    kai.append(date[num3:num3 +prob[6]["eaf1"]])
    num3 += prob[6]["eaf1"]
    kai.append(date[num3:num3 + prob[6]["taf7"]])
    num3 += prob[6]["taf7"]
    kai.append(date[num3:num3 + prob[6]["aff4_kai"]])
    num3 += prob[6]["aff4_kai"]
    kai.append(date[num3:num3 + prob[6]["eaf1_kai"]])
    num3 += prob[6]["eaf1_kai"]
    kai.append(date[num3:num3 + prob[6]["taf7_kai"]])
    new_path = str(args.cluster)[0:-4] + "_dir"
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    thread_list = []
    for i in num:
        thread = multiprocessing.Process(target=cal_multi,
                                         args=(kai, prob, i, new_path, num, result_list),
                                         name=i)
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    f = open(new_path + "/custer_result.txt","w")
    for j1, j2 in zip(result_list, num):
        if j2 == -1:
            j2 = "outlier"
        A = str(j2)
        for j3 in j1:
            A +=  " "
            A += str(j3)
        f.write(A)
        f.write("\n")
    f.close()

    print(num2)



if __name__ == '__main__':
    main()
