query = """
SELECT	C_CUSTKEY,
		C_NAME,
		sum(L_EXTENDEDPRICE * (1 - L_DISCOUNT)) AS REVENUE,
		C_ACCTBAL,
		N_NAME,
		C_ADDRESS,
		C_PHONE,
		C_COMMENT
FROM	'parquet/customer.parquet',
		'parquet/orders.parquet',
		'parquet/lineitem.parquet',
		'parquet/nation.parquet'
WHERE	C_CUSTKEY = O_CUSTKEY
		AND L_ORDERKEY = O_ORDERKEY
		AND O_ORDERDATE >= '1993-10-01'
		AND O_ORDERDATE < '1994-01-01'
		AND L_RETURNFLAG = 'R'
		AND C_NATIONKEY = N_NATIONKEY
GROUP BY 	C_CUSTKEY,
			C_NAME,
			C_ACCTBAL,
			C_PHONE,
			N_NAME,
			C_ADDRESS,
			C_COMMENT
ORDER BY	REVENUE desc
LIMIT 		20
"""
