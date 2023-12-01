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
    connection = None 
    time.sleep(5)
    try:
        conn, cursor = make_db_connection_psycopg2(db_name)
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
