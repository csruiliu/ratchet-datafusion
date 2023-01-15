query = """
SELECT	CNTRYCODE,
		count(*) AS NUMCUST,
		sum(C_ACCTBAL) AS TOTACCTBAL
FROM	(
			SELECT	SUBSTRING(C_PHONE FROM 1 FOR 2) AS CNTRYCODE,
					C_ACCTBAL
			FROM	'parquet/customer.parquet'
			WHERE	SUBSTRING(C_PHONE FROM 1 FOR 2) IN ('13', '31', '23', '29', '30', '18', '17')
					AND C_ACCTBAL > (
						SELECT	AVG(C_ACCTBAL)
						FROM	'parquet/customer.parquet'
						WHERE	C_ACCTBAL > 0.00
								AND SUBSTRING(C_PHONE FROM 1 FOR 2) IN ('13', '31', '23', '29', '30', '18', '17')
					)
					AND NOT EXISTS (
						SELECT	*
						FROM	'parquet/orders.parquet'
						WHERE	O_CUSTKEY = C_CUSTKEY
					)
		) AS CUSTSALE
GROUP BY	CNTRYCODE
ORDER BY	CNTRYCODE
"""
