query = """
SELECT	NATION,
		O_YEAR,
		sum(AMOUNT) AS SUM_PROFIT
FROM	(
			SELECT	N_NAME AS NATION,
   					EXTRACT(YEAR FROM CAST(O_ORDERDATE AS DATE)) AS O_YEAR,
					L_EXTENDEDPRICE * (1 - L_DISCOUNT) - PS_SUPPLYCOST * L_QUANTITY AS AMOUNT
    		FROM	'parquet/part.parquet',
      				'parquet/supplier.parquet',
					'parquet/lineitem.parquet',
					'parquet/partsupp.parquet',
					'parquet/orders.parquet',
					'parquet/nation.parquet'
			WHERE	S_SUPPKEY = L_SUPPKEY
					AND PS_SUPPKEY = L_SUPPKEY
					AND PS_PARTKEY = L_PARTKEY
					AND P_PARTKEY = L_PARTKEY
					AND O_ORDERKEY = L_ORDERKEY
					AND S_NATIONKEY = N_NATIONKEY
					AND P_NAME LIKE '%green%'
		) AS PROFIT
GROUP BY	NATION,
			O_YEAR
ORDER BY	NATION,
			O_YEAR DESC
"""
