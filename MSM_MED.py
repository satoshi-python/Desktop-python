
from msmbuilder.featurizer import DihedralFeaturizer
from msmbuilder.dataset import dataset
from msmbuilder.decomposition import tICA
from msmbuilder.preprocessing import RobustScaler
from msmbuilder.cluster import MiniBatchKMeans
from msmbuilder.lumping import PCCAPlus
from msmbuilder.msm import MarkovStateModel
from msmbuilder.utils import dump
import numpy as np
import msmexplorer as msme
from matplotlib import pyplot as plt
from msmbuilder.utils import load
import tool




def get_option():
    argparser = ArgumentParser()
    argparser.add_argument("-trr", "--trajectory", type=str, help="path of trr")
    argparser.add_argument("-pdb", "--protein", type=str, help="path of pdb")
    argparser.add_argument("-prob", "--probtxt", type=str, help="path of pdb")
    argparser.add_argument("-name", "--name_kei", type=str, help="name of file")
    return argparser.parse_args()

def mak_dihe():
    trr = ["/lustre7/home/lustre3/satoshi/cluster/prepare_msm/tsubame/AFF/TRR/",
          "/lustre7/home/lustre3/satoshi/cluster/prepare_msm/tsubame/EAF/TRR/",
          "/lustre7/home/lustre3/satoshi/cluster/prepare_msm/tsubame/TAF/TRR/"]
    pdb = ["/lustre7/home/lustre3/satoshi/MED/aff4/HEN.pdb",
           "/lustre7/home/lustre3/satoshi/MED/eaf1/HEN.pdb",
           "/lustre7/home/lustre3/satoshi/MED/taf7/HEN.pdb"]
    dir2 = ["aff2_diheds/","eaf2_diheds/","taf2_diheds/"]
    sca_dir = ["aff2_scaled_diheds/","eaf2_scaled_diheds/","taf2_scaled_diheds/"]
    clu_dir = ["aff2_kmeans/","eaf2_kmeans/","taf2_kmeans/"]
    tic = ["aff2_tica/","eaf2_tica/","taf2_tica/"]
    name = ["aff2", "eaf2", "taf2"]
    num = [260, 5, 94]
    for i in range(0, 3):
        TRR = sorted(tool.fail(trr[num], "trr"))
        name1 = ""
        for jj in TRR:
            name1 = str(name1) + " " + str(jj)
        xyz = dataset(name1,
                      topology=pdb[i],
                      stride=2)
        featurizer = DihedralFeaturizer(types=['phi', 'psi'])
        diheds = xyz.fit_transform_with(featurizer, dir2[i], fmt='dir-npy')
        scaler = RobustScaler()
        scaled_diheds = diheds.fit_transform_with(scaler,
                                                  sca_dir[i],
                                                  fmt='dir-npy')
        print(num[i], " :lagtime")
        tica_model = tICA(lag_time=num[i], n_components=4)
        tica_model = scaled_diheds.fit_with(tica_model)
        print(tica_model.score(diheds))
        tica_trajs = scaled_diheds.transform_with(tica_model, tic[i], fmt='dir-npy')
        clusterer = MiniBatchKMeans(n_clusters=20, random_state=42)
        clustered_trajs = tica_trajs.fit_transform_with(
            clusterer, clu_dir[i], fmt='dir-npy'
        )
        msm = MarkovStateModel(lag_time=1, n_timescales=20)
        msm.fit(clustered_trajs)
        print(msm.score(clustered_trajs))
        txx = np.concatenate(xyz)
        assignments = clusterer.partial_transform(txx)
        assignments = msm.partial_transform(assignments)
        fig = plt.figure()
        msme.plot_free_energy(txx, obs=(0, 1), n_samples=100,
                      pi=msm.populations_[assignments],
                      xlabel='tIC 1', ylabel='tIC 2')
        plt.scatter(clusterer.cluster_centers_[msm.state_labels_, 0],
                    clusterer.cluster_centers_[msm.state_labels_, 1],
                    s=1e4 * msm.populations_,       # size by population
                    c=msm.left_eigenvectors_[:, 1], # color by eigenvector
                    cmap="coolwarm",
                    zorder=3
                   )
        plt.colorbar(label='First dynamical eigenvector')
        plt.tight_layout()
        fig.savefig("energy_landscape_{0}.pdf".format(name[i]))




def main():
    mak_dihe()


if __name__ == '__main__':
    main()
