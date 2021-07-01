
from msmbuilder.featurizer import DihedralFeaturizer
from msmbuilder.dataset import dataset
import glob
from argparse import ArgumentParser


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument("-num", "--number", type=str, help="path of pdb")
    return argparser.parse_args()


def main():
    args = get_option()
    pdb = ["/lustre7/home/lustre3/satoshi/MED/aff4/HEN.pdb",
           "/lustre7/home/lustre3/satoshi/MED/eaf1/HEN.pdb",
           "/lustre7/home/lustre3/satoshi/MED/taf7/HEN.pdb"]
    TRR = sorted(glob.glob("*.trr"))
    for i in TRR:
        xyz = dataset(i,
                      topology=pdb[int(args.number)],
                      stride=2)
        print(str(i)[:-4])
        featurizer = DihedralFeaturizer(types=['phi', 'psi'])
        xyz.fit_transform_with(featurizer, str(i)[:-4], fmt='dir-npy')


if __name__ == '__main__':
    main()
