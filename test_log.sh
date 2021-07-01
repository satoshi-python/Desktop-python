
for i in {1..50}
do
    echo $(( i * 10))
    cd cluster_$(( i * 10))
    for file in `\find . -name 'msm_qmrq.sh.o*'`; do
        mkdir txt-1-1000tica-1msm
        python ../test_log-ver2.py -out $file
    done
    cd ../
done
