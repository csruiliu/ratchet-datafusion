query = """
SELECT	sum(L_EXTENDEDPRICE) / 7.0 AS AVG_YEARLY
FROM	'parquet/lineitem.parquet',
		'parquet/part.parquet'
WHERE	P_PARTKEY = L_PARTKEY
		AND P_BRAND = 'Brand#23'
		AND P_CONTAINER = 'MED BOX'
		AND L_QUANTITY < (
			SELECT	0.2 * AVG(L_QUANTITY)
			FROM	'parquet/lineitem.parquet'
			WHERE	L_PARTKEY = P_PARTKEY
		)
"""
