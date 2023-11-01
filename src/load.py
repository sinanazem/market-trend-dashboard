import psycopg2
from psycopg2 import sql
from loguru import logger
from datetime import datetime
from utils import load_yaml_file
import pandas as pd
from extract import extract
import os
import time
def store_data_in_postgresql(data_list):
    connection = None  # Initialize connection to None
    time.sleep(5)

    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host=os.environ.get("POSTGRES_HOST"),
            port=os.environ.get("POSTGRES_PORT"),
            database=os.environ.get("POSTGRES_DB"),
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD")
        )
        logger.info(f"Connecting to PostgreSQL with the following credentials:")
        logger.info(f"Host: {os.environ.get('POSTGRES_HOST')}")
        logger.info(f"Port: {os.environ.get('POSTGRES_PORT')}")
        logger.info(f"Database: {os.environ.get('POSTGRES_DB')}")
        logger.info(f"User: {os.environ.get('POSTGRES_USER')}")

        cursor = connection.cursor()

        # Create the table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS transcripts (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR,
            title VARCHAR,
            date DATE,
            time VARCHAR,
            crawled_date DATE,
            link VARCHAR,
            content TEXT
        )
        """
        cursor.execute(create_table_query)
        connection.commit()

        # Insert data into the table
        insert_query = """
        INSERT INTO transcripts (ticker, title, date, time, crawled_date, link, content)
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
            connection.commit()

        logger.info("Data stored successfully in PostgreSQL database.")

    except (Exception, psycopg2.Error) as error:
        logger.error("Error while connecting to PostgreSQL:", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def main():
    data_list = pd.read_csv("./src/data/fool_earnings.csv").to_dict(orient='index').values()
    store_data_in_postgresql(data_list)
