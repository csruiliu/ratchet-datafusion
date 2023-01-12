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

## CRIU ##

**CRIU** is a utility to checkpoint/restore a process tree. We use it to checkpoint and restore the processes running TPC-H jobs. Then, we compare the end-to-end time of running processes with/without `criu`.

### Installing CRIU from source ###

Install `criu` following their [official page](https://criu.org/Installation), or using our installation [script](./criu_installation.sh). 

## Experiment Results ##

### Local Desktop ###

Query: Q1, Q9, Q21 of TPC-H

Batch Size: 32

SF: 10, 30

Hardware Configuration: 

+ CPU: Intel i9-10900KF (10 Cores / 20 Threads, 3.70GHz-5.30GHz)
+ Memory: 64GB (DDR4, 3200MHz)
+ Disk: Samsung 970 EVO (NVMe, PCIE 3.0)

| SF  | Query | Stop Timing | Runtime (w CR) | CKPT Memory | Runtime (w/o CR) | 
|:---:|:-----:|:-----------:|:--------------:|:-----------:|:----------------:|
| 10  |   1   |     5s      |    50.204s     |     4MB     |     49.579s      |
| 10  |   1   |     15s     |    50.389s     |     4MB     |     49.579s      |
| 10  |   1   |     25s     |    50.548s     |     4MB     |     49.579s      |
| 10  |   1   |     35s     |    50.330s     |     4MB     |     49.579s      |
| 10  |   9   |     7s      |    70.427s     |   73.3MB    |     64.273s      |
| 10  |   9   |     21s     |    68.947s     |   198.3MB   |     64.273s      |
| 10  |   9   |     35s     |    69.697s     |   324.7MB   |     64.273s      |
| 10  |   9   |     49s     |    69.211s     |   2.23GB    |     64.273s      |
| 10  |  21   |     11s     |    113.374s    |   766.7MB   |     107.070s     |
| 10  |  21   |     32s     |    110.876s    |    2.4GB    |     107.070s     |
| 10  |  21   |     54s     |    121.163s    |     9G      |     107.070s     |
| 10  |  21   |     75s     |    117.883s    |     9G      |     107.070s     |
| 30  |   1   |     15s     |    148.316s    |     4MB     |     146.309s     |
| 30  |   1   |     44s     |    147.475s    |     4MB     |     146.309s     |
| 30  |   1   |     73s     |    148.937s    |     4MB     |     146.309s     |
| 30  |   1   |    102s     |    151.575s    |     4MB     |     146.309s     |
| 30  |   9   |     21s     |    222.824     |    208MB    |     212.758s     |
| 30  |   9   |     64s     |    230.980s    |    633MB    |     212.758s     |
| 30  |   9   |    106s     |    228.609s    |    933MB    |     212.758s     |
| 30  |   9   |    149s     |    232.354s    |     4GB     |     212.758s     |
| 30  |  21   |     34s     |    343.079s    |   2.37GB    |     341.760s     |
| 30  |  21   |    103s     |    352.501s    |   6.67GB    |     341.760s     |
| 30  |  21   |    171s     |    387.701s    |   24.7GB    |     341.760s     |
| 30  |  21   |    240s     |    395.778s    |    25GB     |     341.760s     |

### Remote NUC ###

Query: Q1, Q9, Q21 of TPC-H

Batch Size: 32

SF: 10

Hardware Configuration: 

+ CPU: Intel i7-5557U KF (2 Cores / 4 Threads, 3.10GHz)
+ Memory: 16GB
+ Disk： HGST Travelstar 1TB (HDD, SATA II)

| SF  | Query | Stop Timing | Runtime (w/o CR) | Runtime (w CR) | CKPT Memory | CKPT Time |
|:---:|:-----:|:-----------:|:----------------:|:--------------:|:-----------:|:---------:|
| 10  |   1   |     8s      |     78.118s      |    79.241s     |     4M      |  0.227s   |
| 10  |   1   |     23s     |     78.118s      |    79.474s     |     4M      |  0.227s   |
| 10  |   1   |     39s     |     78.118s      |    79.267s     |     4M      |  0.227s   |
| 10  |   1   |     55s     |     78.118s      |    79.509s     |     4M      |  0.222s   |
| 10  |   9   |     12s     |     117.258s     |    119.787s    |    68.3M    |  0.828s   |
| 10  |   9   |     35s     |     117.258s     |    122.567s    |    196M     |  1.851s   |
| 10  |   9   |     59s     |     117.258s     |    123.081s    |   325.3M    |  3.002s   |
| 10  |   9   |     82s     |     117.258s     |    145.818s    |    1.6G     |  14.512s  |
| 10  |  21   |     21s     |     208.420s     |    222.265s    |   866.7M    |  7.689s   |
| 10  |  21   |     63s     |     208.420s     |    256.568s    |    3.1G     |  34.208s  |
| 10  |  21   |    104s     |     208.420s     |    349.733s    |     9G      |  76.507s  |
| 10  |  21   |    146s     |     208.420s     |    351.733s    |     9G      |  78.964s  |