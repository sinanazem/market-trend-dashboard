from crawlers.fool_crawler import FoolStockNewsCrawler
from utils import read_json
from tqdm import tqdm
import pandas as pd
from loguru import logger
import os

from pathlib import Path

def create_folder_if_not_exists(path):
    """
    Create a new folder if it doesn't exists
    """
    Path(path).absolute().mkdir(parents=True, exist_ok=True)


def extract():
    tickers = read_json('./src/static/available_tickers.json')
    list_ = []
    for ticker in tqdm(tickers['tickers'][:10]):
        fool_obj = FoolStockNewsCrawler(ticker)
        list_of_dict = fool_obj.get_transcripts_details()
        list_.extend(list_of_dict)
    return list_



def main():

    create_folder_if_not_exists('./src/data/')
    df = pd.DataFrame(extract())
    df.to_csv('./src/data/fool_earnings.csv', index=False)
    logger.info('stored successfully in  "src/data/fool_earnings.csv"')
