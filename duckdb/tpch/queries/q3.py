query = """
SELECT  L_ORDERKEY,
        sum(L_EXTENDEDPRICE*(1-L_DISCOUNT)) as REVENUE,
        O_ORDERDATE,
        O_SHIPPRIORITY
FROM    'parquet/customer.parquet',
        'parquet/orders.parquet',
        'parquet/lineitem.parquet'
WHERE   C_MKTSEGMENT = 'BUILDING'
        AND C_CUSTKEY = O_CUSTKEY
        AND L_ORDERKEY = O_ORDERKEY
        AND O_ORDERDATE < '1995-03-15'
        AND L_SHIPDATE > '1995-03-15'
GROUP BY    L_ORDERKEY,
            O_ORDERDATE,
            O_SHIPPRIORITY
ORDER BY    REVENUE desc,
            O_ORDERDATE
LIMIT 10
"""
