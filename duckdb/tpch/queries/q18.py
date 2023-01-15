query = """
SELECT	C_NAME,
		C_CUSTKEY,
		O_ORDERKEY,
		O_ORDERDATE,
		O_TOTALPRICE,
		sum(L_QUANTITY)
FROM	'parquet/customer.parquet',
		'parquet/orders.parquet',
		'parquet/lineitem.parquet'
WHERE	O_ORDERKEY IN (
		SELECT	L_ORDERKEY
		FROM	'parquet/lineitem.parquet'
		GROUP BY	L_ORDERKEY 
		HAVING sum(L_QUANTITY) > 300
		)
		AND C_CUSTKEY = O_CUSTKEY
		AND O_ORDERKEY = L_ORDERKEY
GROUP BY	C_NAME,
			C_CUSTKEY,
			O_ORDERKEY,
			O_ORDERDATE,
			O_TOTALPRICE
ORDER BY	O_TOTALPRICE desc,
			O_ORDERDATE
LIMIT 100
"""
