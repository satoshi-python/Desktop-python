
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from argparse import ArgumentParser


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument("-out", "--output", type=str, help="path of pdb")
    return argparser.parse_args()


def txt(path):
    lag_time = []
    msm = []
    name_next = "eaf"
    name_bfore = "aff"
    num_lag = 0
    num_msm = 0
    num1 = 1
    for i in open(path):
        if num_lag == 1:
            num_lag = 0
            lag_time.append(i)
        if "lagtime" in i:
            num_lag = 1
        if "MSM" in i:
            num_msm = 1
        f = i.split()
        if len(f) == 1 and num_msm == 1:
            num_msm = 0
            msm.append(i)
        if len(msm) > 1 and name_bfore in i:
            f = open("txt-1-1000tica-1msm/msm_{0}_{1}.txt".format(name_bfore, num1),"w")
            for k in msm:
                f.write(str(k))
            f.close()
            num1 += 1
            msm = []
        if name_next in i:
            f = open("txt-1-1000tica-1msm/lag_time_{0}.txt".format(name_bfore),"w")
            for k in lag_time:
                f.write(str(k))
            f.close()
            f = open("txt-1-1000tica-1msm/msm_{0}_{1}.txt".format(name_bfore, num1),"w")
            for k in msm:
                f.write(str(k))
            f.close()
            msm = []
            lag_time = []
            num1 += 1
            num1 = 1
            if name_next == "eaf":
                name_next = "taf"
                name_bfore = "eaf"
            elif name_next == "taf":
                name_bfore = "taf"
                name_next = "kkkkkkkkkkkk"
    f = open("txt-1-1000tica-1msm/lag_time_taf.txt", "w")
    for k in lag_time:
        f.write(str(k))
    f.close()
    f = open("txt-1-1000tica-1msm/msm_{0}_{1}.txt".format(name_bfore, num1), "w")
    for k in msm:
        f.write(str(k))
    f.close()


def txt2(path):
    num_tica = 0
    num_msm = 0
    name_li = "aff"
    f = open("txt-1-1000tica-1msm/tica+msm_aff.txt", "w")
    for i in open(path):
        if num_tica == 1:
            tica = float(i)
            num_tica = 0
        if name_li in i:
            num_tica = 1
        if num_msm == 2:
            num_msm = 0
            test = tica + float(i)
            f.write(str(test))
            f.write("\n")
        if len(i.split()) > 4 and "MSM" in i:
            num_msm += 1
        if "eaf" in i and name_li != "eaf":
            f.close()
            f = open("txt-1-1000tica-1msm/tica+msm_eaf.txt", "w")
            name_li = "eaf"
            num_tica = 1
        if "taf" in i and name_li != "taf":
            f.close()
            f = open("txt-1-1000tica-1msm/tica+msm_taf.txt", "w")
            name_li = "taf"
            num_tica = 1
    f.close()


def plot2():
    name = ["aff", "eaf", "taf"]
    for i in name:
        date = []
        fig = plt.figure()
        for i1 in open("txt-1-1000tica-1msm/tica+msm_{0}.txt".format(i)):
            date.append(float(i1))
        print(len(date))
        y = [int(k) for k in range(1, len(date) + 1)]
        plt.scatter(y, date)
        fig.savefig("txt-1-1000tica-1msm/GMRQ_{0}.png".format(i))


def plot():
    name = ["aff", "eaf", "taf"]
    fig = plt.figure(figsize=(15, 5),tight_layout=True)
    score = []
    num1 = 1
    for i in name:
        for j in open("txt-1-1000tica-1msm/lag_time_{0}.txt".format(i)):
            score.append(float(j))
        ax1 = fig.add_subplot(1, 3, num1)
        plt.subplots_adjust(wspace=0.5, hspace=0.5)
        # plt.figure(figsize=(20, 20))
        lag_time = [i1 for i1 in range(1, len(score) + 1)]
        ax1.scatter(lag_time, score)
        ax1.set_ylabel("GMRQ_score")
        ax1.set_xlabel("lag_time")
        ax1.set_title(i)
        score = []
        num1 += 1
    fig.savefig("txt-1-1000tica-1msm/GMRQ_score_tica.pdf")


def plot_msm():
    name = ["aff", "eaf", "taf"]
    score = []
    for i in name:
        fig = plt.figure(figsize=(25, 20), tight_layout=True)
        for j in range(1,21):
            print(j)
            score = []
            for j1 in open("txt-1-1000tica-1msm/msm_{0}_{1}.txt".format(i, j)):
                score.append(float(j1))
            print(max(score))
            ax1 = fig.add_subplot(5, 4, j)
            plt.subplots_adjust(wspace=0.5, hspace=0.5)
            lag_time = [i1 for i1 in range(1, len(score) + 1)]
            ax1.scatter(lag_time, score)
            ax1.set_ylabel("GMRG_score")
            ax1.set_xlabel("MSMlag_time")
            name1 = "tica lag_time" + str(j)
            ax1.set_title(name1)
        fig.savefig("txt-1-1000tica-1msm/GMRQ_score_{0}_msm.pdf".format(i))


def main():
    args = get_option()
    path = str(args.output)
    txt2(path)
    plot2()
    txt(path)
    plot()
    plot_msm()


if __name__ == '__main__':
    main()
