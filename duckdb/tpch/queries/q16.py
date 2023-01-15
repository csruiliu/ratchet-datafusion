query = """
SELECT	P_BRAND,
		P_TYPE,
		P_SIZE,
		count(DISTINCT PS_SUPPKEY) AS SUPPLIER_CNT
FROM	'parquet/partsupp.parquet',
		'parquet/part.parquet'
WHERE	P_PARTKEY = PS_PARTKEY
		AND P_BRAND <> 'Brand#45'
		AND P_TYPE NOT LIKE 'MEDIUM POLISHED%'
		AND P_SIZE IN (49, 14, 23, 45, 19, 3, 36, 9)
		AND PS_SUPPKEY NOT IN (
			SELECT	S_SUPPKEY
			FROM	'parquet/supplier.parquet'
			WHERE	S_COMMENT LIKE '%CUSTOMER%COMPLAINTS%'
		)
GROUP BY	P_BRAND,
			P_TYPE,
			P_SIZE
ORDER BY	SUPPLIER_CNT DESC,
			P_BRAND,
			P_TYPE,
			P_SIZE
"""
