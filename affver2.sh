
export TOOL=/home/biostr1/SOTU18/got/python/tool
export PYTHONPATH=$TOOL:$PYTHONPATH

python cluster_CA-ver2.py -trr /home/biostr1/SOTU18/got/med26_aff4/trr/test_all.trr -pdb /home/biostr1/SOTU18/got/med26_aff4/pdb/HEN.pdb -name aff -prob /home/biostr1/SOTU18/got/med26_aff4/trr/prob.txt
python cluster_CA-ver2.py -trr /home/biostr1/SOTU18/got/Med26_aff4_kai/trr/run_all.trr -pdb /home/biostr1/SOTU18/got/Med26_aff4_kai/aff4kai.pdb -name affkai -prob /home/biostr1/SOTU18/got/Med26_aff4_kai/trr/prob.dat

python cluster_CA-ver2.py -trr /home/biostr1/SOTU18/got/med26_eaf1/trr/test_all.trr -pdb /home/biostr1/SOTU18/got/med26_eaf1/pdb/HEN.pdb -prob /home/biostr1/SOTU18/got/med26_eaf1/trr/prob.txt -name eaf
python cluster_CA-ver2.py -trr /home/biostr1/SOTU18/got/Med26_eaf1_kai/trr/run_all.trr -pdb /home/biostr1/SOTU18/got/Med26_eaf1_kai/eaf1kai.pdb -prob /home/biostr1/SOTU18/got/Med26_eaf1_kai/trr/prob.dat -name eafkai
echo "TAF"
python cluster_CA-ver2.py -trr /home/biostr1/SOTU18/got/med26_taf7/run/test_all.trr -prob /home/biostr1/SOTU18/got/med26_taf7/run/prob.txt -pdb /home/biostr1/SOTU18/got/med26_taf7/pdb/HEN.pdb  -name taf
python cluster_CA-ver2.py -trr /home/biostr1/SOTU18/got/Med26_taf7_kai/trr/run_all.trr -prob /home/biostr1/SOTU18/got/Med26_taf7_kai/trr/prob.dat -pdb /home/biostr1/SOTU18/got/Med26_taf7_kai/taf7kai.pdb  -name tafkai