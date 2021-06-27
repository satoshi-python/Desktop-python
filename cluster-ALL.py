
import satoshi_cluster


def main():
    path = "/lustre7/home/lustre3/satoshi/cluster/ALL/"
    txt = [path + "aff.txt", path + "eaf.txt", path + "taf.txt",
           path + "aff2.txt", path + "eaf3.txt", path + "taf3.txt"]
    test = []
    for name in txt:
        for i in open(name, "r"):
            f = i.split()
            test.append(f)
    PTS = int(len(test)/100)
    EPS = [i * 50 for i in range(2, 41)]
    for eps in EPS:
        kai = satoshi_cluster.db_scan_kai(test, eps, PTS)
        with open("EPS-{0}-PTS-{1}-10**-1.txt".format(eps, PTS), "w") as f:
            for g in kai:
                f.write("%s\n" % g)


if __name__ == '__main__':
    main()
