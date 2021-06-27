
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def get_PROB(path):
    K = [0.0] * 5
    PP = []
    for i in open(path):
        PP.append(float(i))
    # print("PP:",sum(PP))
    if "kai" in path:
        n2 = 201
    else:
        n2 = 181
    for i in range(1, 6):
        for n in range(1, n2):
            K[i-1] += sum(PP[(n-1) * 5000 + 1000 * (i - 1):(n-1) * 5000 + 1000 * i])
            # print((n-1) * 5000 + 1000 * (i - 1),";",(n-1) * 5000 + 1000 * i)
    return K


def get_TXT(path):
    if "kai" in path:
        n1 = 201
    else:
        n1 = 181
    test = []
    for g in range(1, 6):
        kai = [0.0] * 92
        for j in range(1, n1):
            for i in open("{0}_{1}.txt".format(path, ((j-1) * 5) + g)):
                f = i.split()
                for gg in range(92):
                    kai[gg] = float(kai[gg]) + float(f[gg + 1])
        test.append(kai)
    return test


def main():
    home = "/home/biostr1/SOTU18/got/"
    prob_path = [home+"med26_aff4/trr/prob.txt", home + "med26_eaf1/trr/prob.txt",
               home + "med26_taf7/run/prob.txt",home + "Med26_aff4_kai/trr/prob.dat",
               home + "Med26_eaf1_kai/trr/prob.dat", home + "Med26_taf7_kai/trr/prob.dat"]
    txt_path=["TEST/aff","TEST/eaf","TEST/taf","TEST/affkai","TEST/eafkai","TEST/tafkai"]
    # txt_path=["TESTCA/aff","TESTCA/eaf","TESTCA/taf","TESTCA/affkai","TESTCA/eafkai","TESTCA/tafkai"]
    # txt_path=["TESTHY/aff","TESTHY/eaf","TESTHY/taf","TESTHY/affkai","TESTHY/eafkai","TESTHY/tafkai"]
    # txt_path=["TEST2CA/aff","TEST2CA/eaf","TEST2CA/taf","TEST2CA/affkai","TEST2CA/eafkai","TEST2CA/tafkai"]
    PROB_kai = []
    for i in prob_path:
        PROB_kai.append(get_PROB(i))
    TXT = []
    for i in txt_path:
        TXT.append(get_TXT(i))
    fig = plt.figure(figsize=(15, 10), tight_layout=True)
    for i in PROB_kai:
        print(i, "SUM:", sum(i))
    for j1 in range(6):
        ax1 = fig.add_subplot(2, 3, j1 + 1)
        plt.subplots_adjust(wspace=0.5, hspace=0.5)
        plt.figure(figsize=(20, 20))
        a = []
        b = []
        print(TXT[j1])
        for j in range(4):
            a = [((k1 + k2)/(PROB_kai[j1][j] + PROB_kai[j1][j + 1])) * 100  for (k1, k2) in zip(TXT[j1][j],TXT[j1][j + 1])]
            # b = [(k1 + k2) for (k1, k2) in zip(TXT[j1][j], TXT[j1][j + 1])]
            # a = [((k1 + k2)) for (k1, k2) in zip(TXT[j1][j], TXT[j1][j+1])]
            # print(PROB_kai[j1][j] + PROB_kai[j1][j + 1])
            # print(b)
            height = [int(i) for i in range(1, len(a) + 1)]
            b.append(ax1.plot(height, a))
        ax1.set_xlabel("MED26 92 residues")
        ax1.set_ylabel("percentage(%)")
        ax1.set_title(txt_path[j1])
        ax1.legend((b[0][0], b[1][0], b[2][0], b[3][0]),
                   ("0-20", "10-30", "20-40", "30-50"), loc=2)
        # plt.figure(figsize=(20, 20))
    fig.savefig("MED26_CON-TEST2.pdf")
    for j1 in range(6):
        f = open("{0}-CON-TEST2.txt".format(str(txt_path[j1])[5:]), "w")
        print(str(txt_path[j1])[5:])
        A = [float(a + b + c + d + e) for (a,b,c,d,e) in zip(TXT[j1][0],TXT[j1][1],TXT[j1][2],TXT[j1][3],TXT[j1][4])]
        print(len(A))
        for i in A:
            AA = str(i) + "\n"
            f.write(AA)
        f.close()


if __name__ == '__main__':
    main()
