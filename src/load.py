import psycopg2
from psycopg2 import sql
from loguru import logger
from datetime import datetime
from utils import load_yaml_file
import pandas as pd
import os
import time
from src.utils import make_db_connection_psycopg2

def store_data_in_postgresql(data_list, db_name):
    connection = None  # Initialize connection to None
    time.sleep(5)

    try:
        # Connect to the PostgreSQL database
        conn, cursor = make_db_connection_psycopg2(db_name)

        # Insert data into the table
        insert_query = """
        INSERT INTO motley_fool_news (ticker, title, date, time, crawled_date, link, content)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        for data in data_list:
            values = (
                data['ticker'],
                data['title'],
                data['date'],
                data['time'],
                data['crawled_date'],
                data['link'],
                data['content']
            )
            cursor.execute(insert_query, values)
            conn.commit()

        logger.info("Data stored successfully in PostgreSQL database.")

    except (Exception, psycopg2.Error) as error:
        logger.error("Error while connecting to PostgreSQL:", error)

    finally:
        if connection:
            cursor.close()
            conn.close()


# def main():
#     data_list = pd.read_csv("./src/data/fool_earnings.csv").to_dict(orient='index').values()
#     store_data_in_postgresql(data_list)

# if __name__ == "__main__":
#     data_list = pd.read_csv("./src/data/fool_earnings.csv").to_dict(orient='index').values()
#     store_data_in_postgresql(data_list, db_name="market_trends")