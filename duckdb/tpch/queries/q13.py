query = """
SELECT	C_COUNT,
		count(*) AS CUSTDIST
FROM	(
			SELECT	C_CUSTKEY,
					COUNT(O_ORDERKEY)
    		FROM	'parquet/customer.parquet' LEFT OUTER JOIN 'parquet/orders.parquet' ON C_CUSTKEY=O_CUSTKEY AND O_COMMENT 
			NOT LIKE '%special%requests%'
    		GROUP BY	C_CUSTKEY
		) AS C_ORDERS(C_CUSTKEY, C_COUNT)
GROUP BY	C_COUNT
ORDER BY	CUSTDIST desc,
			C_COUNT desc
"""
