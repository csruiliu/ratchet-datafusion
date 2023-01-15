import duckdb
import argparse

from queries import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", 
                        type=str, 
                        action="store", 
                        choices=['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 
                                 'q12', 'q13', 'q14', 'q15', 'q16', 'q17', 'q18', 'q19', 'q20', 'q21', 'q22'], 
                        help="indicate the query id")
    args = parser.parse_args()
    
    qid = args.query
    
    exec_query = globals()[qid].query
    
    con = duckdb.connect(database=':memory:')
    
    if isinstance(exec_query, list):
        for idx, query in enumerate(exec_query):
            if idx == 1:
                results = con.execute(query).fetchdf()
            else:
                con.execute(query)
    else:
        results = con.execute(exec_query).fetchdf()

    print(results)


if __name__ == "__main__":
    main()
