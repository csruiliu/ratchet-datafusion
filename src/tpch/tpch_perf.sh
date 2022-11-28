#!/bin/bash

help_func() {
    echo "Usage:"
    echo "tpch_perf.sh [-q QID] [-b BATCH_SIZE] [-d DATASET_PATH] [-l LOOP]"
    echo "Description:"
    echo "QID, query id of TPC-H benchmark."
    echo "BATCH_SIZE, the batch size of running the benchmark, usually is from 32 to 2^n."
    echo "DATASET_PATH, the dataset for running the benchmark."
    echo "LOOP, the number of loops/iterations."
    exit 0
}

while getopts 'q:b:d:l:h' OPT
do
    case $OPT in
        q) QID="$OPTARG";;
        b) BATCH_SIZE="$OPTARG";;
        d) DATASET_PATH="$OPTARG";;
        l) LOOP="$OPTARG";;
        h) help_func;;
        ?) echo "Unrecognized Parameters"; exit 1;;
    esac
done

sum_time=0.0
itr=1
while [[ $itr -le $LOOP ]]
do
    echo "== Starting $itr iteration =="
    echo "== Cleaning cache =="
    sudo sh -c "/usr/bin/echo 1 > /proc/sys/vm/drop_caches"

    start_time=$(date +%s.%3N)
    cargo run --release --bin tpch -- benchmark --query "$QID" --batch-size "$BATCH_SIZE" --path "$DATASET_PATH" --debug
    end_time=$(date +%s.%3N)

    # elapsed time with millisecond resolution
    # keep three digits after floating point.
    elapsed=$(echo "scale=3; $end_time - $start_time" | bc)
    eval "echo Elapsed Time: $elapsed seconds"
    sum_time=$(echo "$sum_time" + "$elapsed" | bc)
    ((itr = itr + 1))
done

avg_time=$(echo "scale=3; $sum_time/$LOOP" | bc)
eval "echo Elapsed Time: $avg_time seconds on average of $LOOP iteration"
