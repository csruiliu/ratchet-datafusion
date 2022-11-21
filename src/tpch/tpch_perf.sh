
#!/bin/bash
start_time=$(date +%s.%3N)
cargo run --release --bin tpch -- benchmark --query 22 --batch-size 1000 --debug --path ./dataset/sf1
end_time=$(date +%s.%3N)

# elapsed time with millisecond resolution
# keep three digits after floating point.
elapsed=$(echo "scale=3; $end_time - $start_time" | bc)
eval "echo Elapsed Time: $elapsed seconds"
