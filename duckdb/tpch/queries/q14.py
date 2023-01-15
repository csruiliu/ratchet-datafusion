query = """
SELECT	100.00 * sum(CASE WHEN P_TYPE LIKE 'PROMO%'
		THEN L_EXTENDEDPRICE * (1 - L_DISCOUNT) 
		ELSE 0 END) / sum (L_EXTENDEDPRICE * (1 - L_DISCOUNT)) 
		AS PROMO_REVENUE
FROM	'parquet/lineitem.parquet',
		'parquet/part.parquet'
WHERE	L_PARTKEY = P_PARTKEY
		AND L_SHIPDATE >= '1995-09-01'
		AND L_SHIPDATE < '1995-10-01'
"""
