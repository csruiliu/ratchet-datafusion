#!/bin/bash

help_func() {
    echo "Usage:"
    echo "tpch_perf.sh [-q QID] [-b BATCH_SIZE] [-d DATASET_PATH] [-s STOP_TIME] [-l LOOP]"
    echo "Description:"
    echo "QID, query id of TPC-H benchmark."
    echo "BATCH_SIZE, the batch size of running the benchmark, usually is from 32 to 2^n."
    echo "DATASET_PATH, the dataset for running the benchmark."
    echo "STOP_TIME, the timing of stop or suspend the query, you can set multiple timing, like, -s 10 -s 20"
    echo "LOOP, the number of loops/iterations."
    exit 0
}

while getopts 'q:b:d:s:l:h' OPT
do
    case $OPT in
        q) QID="$OPTARG";;
        b) BATCH_SIZE="$OPTARG";;
        d) DATASET_PATH="$OPTARG";;
        s) STOP_TIME+=("$OPTARG");;
        l) LOOP="$OPTARG";;
        h) help_func;;
        ?) echo "Unrecognized Parameters"; exit 1;;
    esac
done

criu_cmd=/usr/local/criu/criu-3.17.1/criu/criu
ckpt_path=/home/ruiliu/Develop/ratchet/ckpt
sum_time=0.0
checkpoint_sum_time=0.0
itr=1
PID=0
while [[ $itr -le $LOOP ]]
do
    echo "== Starting $itr iteration =="
    echo "== Cleaning cache =="
    sudo sh -c "/usr/bin/echo 1 > /proc/sys/vm/drop_caches"

    start_time=$(date +%s.%3N)
    cargo run --release --bin tpch -- benchmark --query "$QID" --batch-size "$BATCH_SIZE" --path "$DATASET_PATH" --debug &
    PID=$!
    # PID=$(ps -ef | grep "target/release/tpch benchmark" | grep -v grep | awk '{print $2}')

    # TODO: support multiple suspends during runtime
    for i in "${!STOP_TIME[@]}"; do
      sleep "${STOP_TIME[$i]}"
      echo "== $i Suspend Job =="

      # checkpoint process into disk
      checkpoint_start_time=$(date +%s.%3N)
      if [ "$i" != 0 ]; then
        PID=$(sudo head -n 1 "$ckpt_path/restore_$((i-1)).pid")
        echo "CRIU Dumps Proc $PID"
      fi

      if [ -d "$ckpt_path/ckpt_${PID}_${i}" ]; then
        echo "Removing and Creating $ckpt_path/ckpt_${PID}_${i} folder."
        sudo rm -rf "$ckpt_path/ckpt_${PID}_${i}"
        mkdir "$ckpt_path/ckpt_${PID}_${i}"
      else
        echo "Creating $ckpt_path/ckpt_${PID}_${i} folder."
        mkdir "$ckpt_path/ckpt_${PID}_${i}"
      fi

      sudo "$criu_cmd" dump -D "$ckpt_path/ckpt_${PID}_${i}" -t "$PID" --shell-job
      echo "Dumping to $ckpt_path/ckpt_${PID}_${i}"

      # force data sync between buffer and disk
      sync
      checkpoint_end_time=$(date +%s.%3N)
      checkpoint_time=$(echo "scale=3; $checkpoint_end_time - $checkpoint_start_time" | bc)

      # clean page cache 
      sudo sh -c "/usr/bin/echo 1 > /proc/sys/vm/drop_caches"

      echo "== $i Resume Job =="
      echo "Restoring from $ckpt_path/ckpt_${PID}_${i}"
      if [ $((i+1)) = ${#STOP_TIME[@]} ]; then
        echo "Final Restore"

        # The following code is used to re-point to /dev/pts/ptmx, but may bring over-mounted issue
        # sudo mount -t devpts -o newinstance lxcpts /dev/pts
        # sudo mount -o bind /dev/pts/ptmx /dev/ptmx

        # restore the process from disk and print out final results
        output=$(sudo "$criu_cmd" restore -D "$ckpt_path/ckpt_${PID}_${i}" --shell-job)
        echo "$output"
      else
        # restore the process from disk and wait for the next suspend
        # --restore-detached is used so that the restored process will be running background
        sudo "$criu_cmd" restore -D "$ckpt_path/ckpt_${PID}_${i}" --pidfile "$ckpt_path/restore_${i}.pid" --shell-job --restore-detached
      fi

      ckpt_size=$(du -sh "$ckpt_path")
      eval "echo Size of CKPT by CRIU: $ckpt_size"
    done
    end_time=$(date +%s.%3N)

    # elapsed time with millisecond resolution
    # keep three digits after floating point.
    elapsed=$(echo "scale=3; $end_time - $start_time" | bc)
    eval "echo Elapsed Time: $elapsed seconds"
    sum_time=$(echo "$sum_time" + "$elapsed" | bc)
    checkpoint_sum_time=$(echo "$checkpoint_sum_time" + "$checkpoint_time" | bc)
    ((itr = itr + 1))
done

avg_time=$(echo "scale=3; $sum_time/$LOOP" | bc)
eval "echo Elapsed Time: $avg_time seconds on average of $LOOP iteration"
checkpoint_avg_time=$(echo "scale=3; $checkpoint_sum_time/$LOOP" | bc)
eval "echo Checkpoint Time: $checkpoint_avg_time seconds on average of $LOOP iteration"