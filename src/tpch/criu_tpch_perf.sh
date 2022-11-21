#!/bin/bash
start_time=$(date +%s.%3N)
cargo run --release --bin tpch -- benchmark --query 3 --batch-size 5 --debug --path ./dataset &
sleep 2
pid=$(ps -ef | grep "target/release/tpch benchmark" | grep -v grep | awk '{print $2}')
sudo /usr/local/criu/criu-3.17.1/criu/criu dump -D /home/ruiliu/Develop/ratchet/ckpt -j -t $pid
sudo /usr/local/criu/criu-3.17.1/criu/criu restore -D /home/ruiliu/Develop/ratchet/ckpt -j
end_time=$(date +%s.%3N)

# elapsed time with millisecond resolution
# keep three digits after floating point.
elapsed=$(echo "scale=3; $end_time - $start_time" | bc)
eval "echo Elapsed Time: $elapsed seconds"


