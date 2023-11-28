import json
import yaml
import psycopg2
from sqlalchemy import create_engine
import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
import os
from loguru import logger

def read_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data

import yaml

def load_yaml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except Exception as e:
        print(f"Error loading YAML file '{file_path}': {e}")
        return None


def make_db_connection_psycopg2(database: str, autocommit: bool = False):

    #assert database in list(conn_dict.keys()), "server couldn't be recognized in the config file"

    
    database=os.environ.get("POSTGRES_DB") if database is None else database

    host=os.environ.get("POSTGRES_HOST")
    port=os.environ.get("POSTGRES_PORT")
    user=os.environ.get("POSTGRES_USER")
    password=os.environ.get("POSTGRES_PASSWORD")
    
    conn = psycopg2.connect(user=user, password=password, host=host, dbname=database)
    cursor = conn.cursor()

    if autocommit:
        conn.autocommit = True

    return conn, cursor


def make_db_connection_alchemy(database: str, autocommit: bool = False):
    #assert database in list(conn_dict.keys()), "provided server couldn't be recognized in the config file"
    database=os.environ.get("POSTGRES_DB") if database is None else database

    host=os.environ.get("POSTGRES_HOST")
    port=os.environ.get("POSTGRES_PORT")
    user=os.environ.get("POSTGRES_USER")
    password=os.environ.get("POSTGRES_PASSWORD")

    engine = create_engine('postgresql+psycopg2://' + user + ':' + password + '@' + host + ':5432/' + database)

    metadata2 = sq.MetaData(engine)
    Base = declarative_base(metadata=metadata2)

    session_maker = sq.orm.sessionmaker(bind=engine, autocommit=autocommit)
    session = session_maker()

    return session, Base


def make_db_connection_engine(database: str):
    #assert database in list(conn_dict.keys()), "provided server couldn't be recognized in the config file"

    database=os.environ.get("POSTGRES_DB") if database is None else database

    host=os.environ.get("POSTGRES_HOST")
    port=os.environ.get("POSTGRES_PORT")
    user=os.environ.get("POSTGRES_USER")
    password=os.environ.get("POSTGRES_PASSWORD")

    engine = create_engine('postgresql+psycopg2://' + user + ':' + password + '@' + host + ':5432/' + database)

    return engine

if __name__ == "__main__":
    
    query = """
    CREATE TABLE test(
        id SERIAL Primary Key,
        name VARCHAR(50)
        ); 
        """
    conn, cursor = make_db_connection_psycopg2("postgres")
    cursor.execute(query)
    conn.commit()
    