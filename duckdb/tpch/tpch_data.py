import os
import pandas as pd
import argparse
from datetime import date
 

def main(): 
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--table", type=str, action="store", help="indicate the name of table that needs to be converted to parquet")
    args = parser.parse_args()
    
    tbl_name = args.table
    
    dataset_folder = "/home/ruiliu/Develop/ratchet/duckdb/tpch/tbl"
    
    # Column names of each table
    part_cols = ["P_PARTKEY", "P_NAME", "P_MFGR", "P_BRAND", "P_TYPE", "P_SIZE", "P_CONTAINER", "P_RETAILPRICE", "P_COMMENT"]
    supplier_cols = ["S_SUPPKEY", "S_NAME", "S_ADDRESS", "S_NATIONKEY", "S_PHONE", "S_ACCTBAL", "S_COMMENT"]
    partsupp_cols = ["PS_PARTKEY", "PS_SUPPKEY", "PS_AVAILQTY", "PS_SUPPLYCOST", "PS_COMMENT"]
    customer_cols = ["C_CUSTKEY", "C_NAME", "C_ADDRESS", "C_NATIONKEY", "C_PHONE", "C_ACCTBAL", "C_MKTSEGMENT", "C_COMMENT"]
    orders_cols = ["O_ORDERKEY", "O_CUSTKEY", "O_ORDERSTATUS", "O_TOTALPRICE", "O_ORDERDATE", "O_ORDERPRIORITY", "O_CLERK", "O_SHIPPRIORITY", "O_COMMENT"]
    lineitem_cols = ["L_ORDERKEY", "L_PARTKEY", "L_SUPPKEY", "L_LINENUMBER", 
                     "L_QUANTITY", "L_EXTENDEDPRICE", "L_DISCOUNT", "L_TAX", 
                     "L_RETURNFLAG", "L_LINESTATUS", "L_SHIPDATE", "L_COMMITDATE", 
                     "L_RECEIPTDATE", "L_SHIPINSTRUCT", "L_SHIPMODE", "L_COMMENT"]
    nation_cols = ["N_NATIONKEY", "N_NAME", "N_REGIONKEY", "N_COMMENT"]
    region_cols = ["R_REGIONKEY", "R_NAME", "R_COMMENT"]
    
    # Schema of each table
    part_schame = {"P_PARTKEY":int, "P_NAME":str, "P_MFGR":str, 
                   "P_BRAND":str, "P_TYPE":str, "P_SIZE":int, 
                   "P_CONTAINER":str, "P_RETAILPRICE":float, "P_COMMENT":str}
    supplier_schema = {"S_SUPPKEY":int, "S_NAME":str, "S_ADDRESS":str, 
                       "S_NATIONKEY":int, "S_PHONE":str, "S_ACCTBAL":float, "S_COMMENT":str}
    partsupp_schema = {"PS_PARTKEY":int, "PS_SUPPKEY":int, "PS_AVAILQTY":int, "PS_SUPPLYCOST":float, "PS_COMMENT":str}
    customer_schema = {"C_CUSTKEY":int, "C_NAME":str, "C_ADDRESS":str, "C_NATIONKEY":int, 
                       "C_PHONE":str, "C_ACCTBAL":float, "C_MKTSEGMENT":str, "C_COMMENT":str}
    orders_schema = {"O_ORDERKEY":int, "O_CUSTKEY":int, "O_ORDERSTATUS":str, "O_TOTALPRICE":float, 
                     "O_ORDERDATE":date, "O_ORDERPRIORITY":str, "O_CLERK":str, "O_SHIPPRIORITY":int, "O_COMMENT":str}
    lineitem_schema = {"L_ORDERKEY":int, "L_PARTKEY":int, "L_SUPPKEY":int, "L_LINENUMBER":int, 
                       "L_QUANTITY":float, "L_EXTENDEDPRICE":float, "L_DISCOUNT":float, "L_TAX":float, 
                       "L_RETURNFLAG":str, "L_LINESTATUS":str, "L_SHIPDATE":date, "L_COMMITDATE":date, 
                       "L_RECEIPTDATE":date, "L_SHIPINSTRUCT":str, "L_SHIPMODE":str, "L_COMMENT":str}
    nation_schema = {"N_NATIONKEY":int, "N_NAME":str, "N_REGIONKEY":int, "N_COMMENT":str}
    region_schema = {"R_REGIONKEY":int, "R_NAME":str, "R_COMMENT":str}
    
    
    col_name = None
    col_schema = None
    
    if tbl_name != None:
        if tbl_name == "part":
            print("It is part table")
            col_name = part_cols
        elif tbl_name == "supplier":
            print("It is supplier table")
            col_name = supplier_cols
        elif tbl_name == "partsupp":
            print("It is partsupp table")
            col_name = partsupp_cols
        elif tbl_name == "customer":
            print("It is customer table")
            col_name = customer_cols
        elif tbl_name == "orders":
            print("It is orders table")
            col_name = orders_cols
        elif tbl_name == "lineitem":
            print("It is lineitem table")
            col_name = lineitem_cols
        elif tbl_name == "nation":
            print("It is nation table")
            col_name = nation_cols
        elif tbl_name == "region":
            print("It is region table")
            col_name = region_cols
        
        file_name = os.path.join(dataset_folder, tbl_name)
            
        df = pd.read_csv(filepath_or_buffer=file_name+'.tbl', delimiter="|", index_col=False, names=col_name)
        df.to_parquet(file_name + ".parquet")
        
    else:
        for f in os.listdir(dataset_folder):
            if f == "part.tbl":
                print("It is part table")
                col_name = part_cols
            elif f == "supplier.tbl":
                print("It is supplier table")
                col_name = supplier_cols
            elif f == "partsupp.tbl":
                print("It is partsupp table")
                col_name = partsupp_cols
            elif f == "customer.tbl":
                print("It is customer table")
                col_name = customer_cols
            elif f == "orders.tbl":
                print("It is orders table")
                col_name = orders_cols
            elif f == "lineitem.tbl":
                print("It is lineitem table")
                col_name = lineitem_cols
            elif f == "nation.tbl":
                print("It is nation table")
                col_name = nation_cols
            elif f == "region.tbl":
                print("It is region table")
                col_name = region_cols
        
            file_name = os.path.join(dataset_folder, f)
            if os.path.isfile(file_name):
                df = pd.read_csv(filepath_or_buffer=file_name, delimiter="|", index_col=False, names=col_name)
                df.to_parquet(file_name.split('.', 1)[0] + ".parquet")
            
    
if __name__ == "__main__":
    main()
