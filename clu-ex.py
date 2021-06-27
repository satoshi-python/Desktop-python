from argparse import ArgumentParser
import os
import random
import tool

def PROB():
    home = "/lustre7/home/lustre3/satoshi/MED/"
    path = [home + "aff4/prob.txt", home + "eaf1/prob.txt", home + "taf7/prob.txt",
            home + "aff4_kai/prob.dat",home + "eaf1_kai/prob.dat",home + "taf7_kai/prob.dat"]
    prob = {}
    kai = []
    REB = {}
    for name in path:
        for (t, num)  in zip(open(name), range(1, 1000001)):
            if float(t) >= 10 ** -10:
                prob[num] = float(t)
        print(name[34:-9])
        REB[name[34:-9]] = len(prob)
        kai.append(prob)
        prob = {}
    kai.append(REB)
    return kai


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument("-txt", "--cluster", type=str, help="name of file")
    return argparser.parse_args()


def main():
    prob = PROB()
    args = get_option()
    date = []
    print(str(args.cluster))
    for i in open(str(args.cluster)):
        date.append(int(i))
    num = list(set(date))
    kai = []
    num3 = 0
    kai.append(date[num3:num3 + prob[6]["aff4"]])
    num3 += prob[6]["aff4"]
    kai.append(date[num3:num3 + prob[6]["eaf1"]])
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
    name = ["aff4.txt","eaf.txt","taf.txt","affkai.txt","eafkai.txt","tafkai.txt"]
    num2 = 0
    MM = "/lustre7/home/lustre3/satoshi/MED/"
    TRR_path = [MM + "aff4/test_all.trr", MM + "eaf1/test_all.trr", MM + "taf7/test_all.trr",
                MM + "aff4_kai/run_all.trr", MM + "eaf1_kai/run_all.trr", MM + "taf7_kai/run_all.trr"]
    pdb_path = [MM + "aff4/HEN.pdb", MM + "eaf1/HEN.pdb", MM + "taf7/HEN_msm.pdb",
                MM + "aff4_kai/aff4kai.pdb", MM + "eaf1_kai/eaf1kai.pdb", MM + "taf7_kai/taf7kai.pdb"]
    test_kai = []
    for i in num:
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
        num2 += sum(S_list)
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
                tool.TRR_TO_PDB(TRR_path[j],pdb_path[j],random.sample(test[j], 10),new_path3)
        test_kai.append(S_list)
    f = open(new_path + "/custer_result.txt","w")
    for j1, j2 in zip(test_kai, num):
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
