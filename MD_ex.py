
import tool
from argparse import ArgumentParser
import numpy as np
import random
import os


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument("-name", "--name_kai", type=str, help="name of file")
    return argparser.parse_args()


def SEP_list(LIST):
    num = 0
    kai = [[] for i in range(20)]
    for j1, j2 in zip(LIST, range(5001)):
        num += 1
        kai[j1].append(j2 * 2)
    print(num)
    return kai


def main():
    trr = ["/lustre7/home/lustre3/satoshi/cluster/prepare_msm/tsubame/AFF/TRR/",
          "/lustre7/home/lustre3/satoshi/cluster/prepare_msm/tsubame/EAF/TRR/",
          "/lustre7/home/lustre3/satoshi/cluster/prepare_msm/tsubame/TAF/TRR/"]
    pdb = ["/lustre7/home/lustre3/satoshi/MED/aff4/HEN.pdb",
           "/lustre7/home/lustre3/satoshi/MED/eaf1/HEN.pdb",
           "/lustre7/home/lustre3/satoshi/MED/taf7/HEN.pdb"]
    clu = ["/lustre7/home/lustre3/satoshi/MSM/MED/result/aff2_kmeans/",
           "/lustre7/home/lustre3/satoshi/MSM/MED/result/eaf2_kmeans/"
           "/lustre7/home/lustre3/satoshi/MSM/MED/result/taf2_kmeans/"]
    args = get_option()
    if str(args.name_kai) ==  "taf":
        num = 2
    elif str(args.name_kai) ==  "eaf":
        num = 1
    elif  str(args.name_kai) ==  "aff":
        num = 0
    TEST = [] * 20
    TRR = sorted(tool.fail(trr[num], "trr"))
    print(len(TRR))
    for i in range(100):
        print(TRR[i])
        kai = clu[num] + str(str(i).zfill(8)) + ".npy"
        NUM = SEP_list(list(np.load(kai)))
        name = "cluster_"  + str(args.name_kai)
        if not os.path.exists(name):
            os.mkdir(name)
        name =  name + "/" + str(TRR[i])[:-4].replace(trr[num], "")
        if not os.path.exists(name):
            os.mkdir(name)
        path_trr = TRR[i]
        NNN = 0
        for j in NUM:
            NNN += 1
            if len(j) > 10:
                name1 = name + "/" + str(NNN)
                if not os.path.exists(name1):
                    os.mkdir(name1)
                # tool.TRR_TO_PDB(path_trr, pdb[num], random.sample(j, 10),name1 + "/")


if __name__ == '__main__':
    main()
