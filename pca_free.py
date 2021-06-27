
import pandas as pd
import seaborn as sns
import statistics
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

path = "/home/satoshi/ALL_PCA/txt/"
file_txt = ["aff.txt", "eaf.txt", "taf.txt", "affkai.txt", "eafkai.txt", "tafkai.txt"]

class FREE_ENERGY_LANDSCAPE:
    def ____init__(self):
        self.MED = []
        self.num_CAL_ENERGY = 0
        self.num_prob = []
        self.kai = []
    def REAS_result_txt(self, txt):
        x = []
        y = []
        kai = []
        for i in open(txt):
            f = i.split()
            x.append(f[0])
            y.append(f[1])
            self.prob_num += 1
        kai.append(x)
        kai.append(y)
        self.MED.append(kai)
    #calculation prob
    def CAL1(self,txt="a"):
        if txt == "a":
            self.num_prob += [float(1/self.num_prob)] * self.num_prob
        else:
            for i in open(txt):
                self.num_prob.append(float(i))
    #calcuklation free energy
    def CAL2(self):
        #kai = np.array(self.MED)
        num1 = 0
        for i in self.MED:
            num1 += len(i[0])
        if self.num_CAL_ENERGY == 1:
            print("We have already calcuration")
            self.num_CAL_ENERGY += 1
        elif self.num_CAL_ENERGY == 2:
            print("restart FREE_ENERGY_LANDSCAPE")
        elif num1 != self.num_prob:
            print("tne prob number if different from TRR file")
        else:
            self.num_CAL_ENERGY += 1
            num2 = 0
            for i in range(len(self.MED)):
                for j in range(len(self.MED[i][0])):
                    self.kai.append(math.log(self.num_prob[num2]) * (-1.986) * 0.3)  # log(prob)*R*T
                    num2 += 1
    def CAL3(self, kizami):
        self.kizmai = kizami
        clt = [[0.0 for i in range(kizami)]for j in range(kizami)]
        x_min = []
        x_max = []
        y_min = []
        y_max = []
        x = []
        y = []
        for i in range(len(self.MED)):
            for j in range(len(self.MED[i][0])):
                y += self.MED[i][1]
                x += self.MED[i][0]
        x_min = min(x)
        x_max = max(x)
        y_min = min(y)
        y_max = max(y)
        self.x = x
        self.y = y
        x_jiku = (x_max - x_min)
        y_jiku = (y_max - y_min)
        x_haba = x_jiku/kizami
        y_haba = y_jiku/kizami
        for i in range(kizami):
            x3 = (x_haba * i) + x_min
            x.append(x3)
            y3 = (y_haba + i) + y_min
            y.append(y3)
        for j6 in range(self.prob_num):
            clt[kizami - (int((y[j6] - y_min)/y_haba)+1)][(int((x[j6] - x_min)/x_haba) - 1)] += float(self.kai[j6])
        self.clt = clt

        def draw_map(self, title="heat map", x_label="x", y_label="y", file_path="heat_sample.png"):
            MAX = np.amax(np.array(self.clt))
            df = pd.DataFrame(clt,
                            index=range(1, int(self.kizami) + 1),
                            columns=range(1, int(self.kizami) + 1))
            df_mask = (df <= statistics.median(self.prob))
            clt1 = []
            for i in self.clt:
                for j in self.clt[i]:
                    clt1.append(j)
            ax = sns.heatmap(df, cmap="jet", vmin=statistics.median(clt1), vmax=MAX, mask=df_mask, cbar_kws={'label': str(title)})
            ax.grid()
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            #plt.figure(figsize=(20,10))
            plt.show()
            plt.savefig("{0}".format(file_path))
            plt.close()
