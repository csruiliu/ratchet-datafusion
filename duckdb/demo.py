import duckdb


def main(): 
    query = """
    SELECT  L_RETURNFLAG,
            L_LINESTATUS,
            sum(L_QUANTITY) as SUM_QTY,
            sum(L_EXTENDEDPRICE) as SUM_BASE_PRICE,
            sum(L_EXTENDEDPRICE * (1 - L_DISCOUNT)) as SUM_DISC_PRICE,
            sum(L_EXTENDEDPRICE * (1 - L_DISCOUNT) * (1 + L_TAX)) as SUM_CHARGE,
            avg(L_QUANTITY) as AVG_QTY,
            avg(L_EXTENDEDPRICE) as AVG_PRICE,
            avg(L_DISCOUNT) as AVG_DISC,
            count(*) as COUNT_ORDER
    FROM    'tpch/parquet/lineitem.parquet'
    WHERE   L_SHIPDATE <= '1998-09-16'
    GROUP BY L_RETURNFLAG, L_LINESTATUS
    ORDER BY L_RETURNFLAG, L_LINESTATUS
    """
    
    cursor = duckdb.connect(database=':memory:')
    results = cursor.execute_suspend(query, 1).fetchdf()
    
    print(results)
    
if __name__ == "__main__":
    main()