query = """
SELECT	SUPP_NATION,
		CUST_NATION,
		L_YEAR,
		sum(VOLUME) AS REVENUE
FROM	(
			SELECT	N1.N_NAME AS SUPP_NATION,
					N2.N_NAME AS CUST_NATION,
					EXTRACT(YEAR FROM CAST(L_SHIPDATE AS DATE)) AS L_YEAR,
					L_EXTENDEDPRICE * (1 - L_DISCOUNT) AS VOLUME
			FROM	'parquet/supplier.parquet',
					'parquet/lineitem.parquet',
					'parquet/orders.parquet',
					'parquet/customer.parquet',
					'parquet/nation.parquet' n1,
					'parquet/nation.parquet' n2
			WHERE	S_SUPPKEY = L_SUPPKEY
					AND O_ORDERKEY = L_ORDERKEY
					AND C_CUSTKEY = O_CUSTKEY
					AND S_NATIONKEY = n1.N_NATIONKEY
					AND C_NATIONKEY = n2.N_NATIONKEY
					AND(
						(n1.N_NAME='FRANCE' AND n2.N_NAME='GERMANY') OR (n1.N_NAME='GERMANY' AND n2.N_NAME='FRANCE')
					)
					AND L_SHIPDATE BETWEEN '1995-01-01' AND '1996-12-31'
    	) AS SHIPPING
GROUP BY	SUPP_NATION,
			CUST_NATION,
			L_YEAR
ORDER BY	SUPP_NATION,
			CUST_NATION,	
			L_YEAR
"""
