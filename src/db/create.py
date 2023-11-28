import os
import sys
import os
import pandas as pd
from sqlalchemy import create_engine
from loguru import logger
from src.utils import make_db_connection_psycopg2, make_db_connection_engine

def drop_database(db_name, new_db_name):
    
    # Create Database
    query = f"DROP DATABASE {new_db_name}"
    
    # "None" because i want connect to default db
    conn, cursor = make_db_connection_psycopg2(database=db_name)
    conn.autocommit = True
    cursor.execute(query)
    conn.commit()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()

def create_database(db_name, new_db_name):
    
    # Create Database
    query = f"CREATE DATABASE {new_db_name}"
    
    # "None" because i want connect to default db
    conn, cursor = make_db_connection_psycopg2(database=db_name)
    conn.autocommit = True
    cursor.execute(query)
    conn.commit()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()
    
    

def create_schema(schema_name, dbname: str):
    query = f"create schema if not exists {schema_name}"
    conn, cursor = make_db_connection_psycopg2(dbname, autocommit=False)
    cursor.execute(query)
    conn.commit()


def drop_tables(dbname: str):
    query = "drop table if exists symbols.nasdaq_screener; " \
            "drop table if exists motley_fool_news; "
    conn, cursor = make_db_connection_psycopg2(dbname, autocommit=False)
    cursor.execute(query)
    conn.commit()

def motley_fool_news_table(dbname: str):
    query = "CREATE TABLE IF NOT EXISTS motley_fool_news (" \
            "id SERIAL PRIMARY KEY, " \
            "ticker VARCHAR, " \
            "title VARCHAR, " \
            "date DATE, " \
            "time VARCHAR, " \
            "crawled_date DATE, " \
            "link VARCHAR, " \
            "content TEXT);"
    conn, cursor = make_db_connection_psycopg2(dbname, autocommit=False)
    cursor.execute(query)
    conn.commit()
    


def insert_static_data(dbname: str):
    
    engine = make_db_connection_engine(dbname)
    # Nasdaq Symbols
    csv_path = "src/db/nasdaq_screener.csv"
    df = pd.read_csv(csv_path)
    df.to_sql("nasdaq_screener", engine, schema="symbols", index=False, if_exists='replace')


def main():
    drop_database("postgres","market_trends")
    create_database("postgres","market_trends")
    logger.info("db is created!")
    
    create_schema(schema_name="symbols", dbname="market_trends")
    logger.info("Symbols schema created")
    
    drop_tables("market_trends")
    motley_fool_news_table("market_trends")

    insert_static_data("market_trends")
    logger.info("Static data inserted")
    
if __name__ == '__main__': 
    main()
