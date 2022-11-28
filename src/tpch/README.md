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

### Experiment Results ###

Query: Q1, Q9, Q21 of TPC-H

Batch Size: 32

SF: 10, 30

Hardware Configuration: 

+ CPU: Intel-10900KF (10 Cores / 20 Threads, 3.70GHz-5.30GHz)
+ Memory: 64GB (3200MHz)
+ Disk: Samsung 970 EVO (PCIE 3.0)

| SF | Query | Stop Timing | Runtime (w CR) | CKPT Memory | Runtime (w/o CR) |
|:--:|:-----:|:-----------:|:--------------:|:-----------:|:----------------:|
| 10 |   1   |     5s      |    50.204s     |     4MB     |     49.579s      |
| 10 |   1   |     15s     |    50.389s     |     4MB     |     49.579s      |
| 10 |   1   |     25s     |    50.548s     |     4MB     |     49.579s      |
| 10 |   1   |     35s     |    50.330s     |     4MB     |     49.579s      |
| 10 |   9   |     7s      |    69.247s     |   73.3MB    |     69.851s      |
| 10 |   9   |     21s     |    68.947s     |   198.3MB   |     69.851s      |
| 10 |   9   |     35s     |    69.697s     |   324.7MB   |     69.851s      |
| 10 |   9   |     49s     |    69.211s     |   2.23GB    |     69.851s      |
| 10 |  21   |     11s     |    113.374s    |   766.7MB   |     107.070s     |
| 10 |  21   |     32s     |    110.876s    |    2.4GB    |     107.070s     |
| 10 |  21   |     54s     |    121.163s    |     9G      |     107.070s     |
| 10 |  21   |     75s     |    117.883s    |     9G      |     107.070s     |
| 30 |   1   |     15s     |    147.448s     |      1.17G    |     146.309s     |
| 30 |   1   |          |         |          |     146.309s   |
| 30 |   1   |          |         |          |     146.309s    |
| 30 |   1   |          |         |          |     146.309s     |
| 30 |   9   |           |         |       |     212.758s      |
| 30 |   9   |          |         |      |      212.758s     |
| 30 |   9   |          |         |      |      212.758s     |
| 30 |   9   |          |        |       |     212.758s     |
| 30 |   21   |     34s      |         |       |     341.760s      |
| 30 |   21  |     103s     |         |      |      341.760s     |
| 30 |   21   |    171s      |    387.701    |   24.7GB   |      341.760s     |
| 30 |   21   |     240s     |        |       |     341.760s     |

