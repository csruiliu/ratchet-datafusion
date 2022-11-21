# TPC-H Benchmark

Running Arrow-Datafusion on TPC-H Benchmark.

TPC-H queries are defined [here](./queries). 

TPC-H dataset that are generated using `dbgen` in [tpch](https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp) are store [here](./dataset).

The command example is like:

```bash
cargo run --release --bin tpch -- benchmark --query 1 --path ./dataset/sf1
```

The command has multiple parameters:

+ **query**: query_id from 1 to 22, will run all TPC-H queries if no `query`. 
+ **debug**: if the debug is enabled
+ **iterations**: Number of iterations for running TPC-H experiments
+ **partitions**: Number of partitions to process in parallel
+ **batch-size**: Batch size when reading CSV or Parquet files (usually from 32 to 2^n, may get `ArrorError(Empty iterator passed to ScalarValue::iter_to_array)`)
+ **path (Required)**: Path to data files.
+ **format**: File format: `csv` or `parquet`
+ **mem_table**: Load the data into a MemTable before executing the query
+ **output**: Path to output directory where JSON summary file should be written to
+ **disable_statistics**: Whether to disable collection of statistics (and cost based optimizations) or not.