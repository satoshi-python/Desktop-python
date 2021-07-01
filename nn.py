
import numpy as np
from argparse import ArgumentParser

def get_option():
    argparser = ArgumentParser()
    argparser.add_argument("-path", "--path", type=str, help="path of pdb")
    return argparser.parse_args()

def main():
    args = get_option()
    test = []
    for i in range(100):
        test.append(list(np.load(args.path + str(str(i).zfill(8)) + ".npy")[0]))
    for i in range(100):
        kai = list(np.load(str(str(i).zfill(4)) + ".npy")[0])
        for j in range(len(test)):
            # print(kai[0])
            # print(test[j][0])
            if test[j][0] == kai[0]:
                print(i, j)

if __name__ == '__main__':
    main()
