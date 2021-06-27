
import tool
import os
import multiprocessing


MM = "/home/biostr1/SOTU18/got"
TRR_path = [MM + "/med26_aff4/trr/test_all.trr", MM + "/med26_eaf1/trr/test_all.trr", MM + "/med26_taf7/run/test_all.trr",
            MM + "/Med26_aff4_kai/trr/run_all.trr", MM + "/Med26_eaf1_kai/trr/run_all.trr", MM + "/Med26_taf7_kai/trr/run_all.trr"]
pdb_path = [MM + "/med26_aff4/pdb/HEN.pdb", MM + "/med26_eaf1/pdb/HEN.pdb", MM + "/med26_taf7/pdb/HEN.pdb",
            MM + "/Med26_aff4_kai/aff4kai.pdb", MM + "/Med26_eaf1_kai/eaf1kai.pdb", MM + "/Med26_taf7_kai/taf7kai.pdb"]
path = [MM + "/med26_aff4/trr/prob.txt", MM + "/med26_eaf1/trr/prob.txt", MM + "/med26_taf7/run/prob.txt",
        MM + "/Med26_aff4_kai/trr/prob.dat", MM + "/Med26_eaf1_kai/trr/prob.dat", MM + "/Med26_taf7_kai/trr/prob.dat"]


def cluster(*path1):
    print("start :", path1)
    path = ""
    for i in path1:
        path += str(i)
    fail = tool.fail(path + "/", "txt")
    for name in fail:
        List = []
        print(name)
        for i in open(name, "r"):
            List.append(float(i))
        if "affkai" in name:
            num = 3
            ff = path + "/affkai.png"
        elif "aff4" in name:
            num = 0
            ff = path + "/aff.png"
        elif "eafkai" in name:
            num = 4
            ff = path + "/eafkai.png"
        elif "eaf" in name:
            num = 1
            ff = path + "/eaf.png"
        elif "tafkai" in name:
            num = 5
            ff = path + "/tafkai.png"
        elif "taf" in name:
            num = 2
            ff = path + "/tag.png"
        kai = tool.MD_LIST_CONTACT(pdb_path[num], TRR_path[num],
                                   path[num], name)
        tool.heat_map(ff, "prob(%)", "MED26NTD", ff[:-4], kai)
        print("end:", path1)


def main():
    path = "/"
    tool.fail(path, "txt")
    name = os.listdir(path=".")
    thread_list = []
    for i in name:
        if ".txt" not in i or ".py" not in i or ".sh" not in i:
            thread = multiprocessing.Process(target=cluster,
                                             args=(str(i)),
                                             name=i)
            thread.start()
            thread_list.append(thread)
            if len(thread_list) > 100:
                for thread in thread_list:
                    thread.join()
                thread_list = []
    for thread in thread_list:
        thread.join()


if __name__ == '__main__':
    main()
