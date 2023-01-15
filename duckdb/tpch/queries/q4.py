query = """
SELECT  O_ORDERPRIORITY,
		count(*) AS ORDER_COUNT
FROM    'parquet/orders.parquet'
WHERE   O_ORDERDATE >= '1993-07-01'
		AND O_ORDERDATE < '1993-10-01'
		AND EXISTS(
	    	SELECT *
	    	FROM 'parquet/lineitem.parquet'
	    	WHERE L_ORDERKEY = O_ORDERKEY
	     	AND L_COMMITDATE < L_RECEIPTDATE
		)
GROUP BY O_ORDERPRIORITY
ORDER BY O_ORDERPRIORITY
"""
