import requests
from bs4 import BeautifulSoup
from datetime import datetime
from loguru import logger
import re
from tqdm import tqdm
import time

BASE_URL = 'https://www.fool.com'
class FoolStockNewsCrawler:
    def __init__(self, ticker):
        self.ticker = ticker
    def get_earning_urls(self):
        url = f"https://www.fool.com/quote/nasdaq/{self.ticker}/"
        logger.info(url)

        earning_call_links = []
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad response status
            soup = BeautifulSoup(response.text, "html.parser")
            html_link_list = soup.find(id="news-analysis-container").find_all("a")

            for link in html_link_list:
                earning_call_links.append(BASE_URL + link['href'])
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        return earning_call_links

    def crawl_transcripts_detailes(self, url):
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad response status

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find('h1').text if soup.find('h1') else ''
        ticker = soup.find('a', {'class': 'ticker-symbol'}).text if soup.find('a', {'class': 'ticker-symbol'}) else ''
        content = soup.find(class_='tailwind-article-body').text if soup.find(class_='tailwind-article-body') else ''

        date_match = re.search(r'([A-Za-z]{3}\s\d{1,2},\s\d{4})\s+at\s+(\d{1,2}:\d{2}[APM]{2})', response.text)
        if date_match:
            date = date_match.group(1)
            time = date_match.group(2)
        else:
            date = ''
            time = ''

        detail_transcripts_dict = {
            'ticker': self.ticker,
            'title': title,
            'date': date,
            'time': time,
            'crawled_date': datetime.today(),
            'link': url,
            'content': content,
        }
        return detail_transcripts_dict


    def get_transcripts_details(self):
        links = self.get_earning_urls()
        if links:
            logger.info(f'{self.ticker} URLs crawled!')
        else:
            logger.error(f'{self.ticker} URLs lists is empty!')

        data_list = [self.crawl_transcripts_detailes(link) for link in links]
        logger.info(f'{self.ticker} transcripts detailes crawled!')
        return data_list


if __name__ == "__main__":
    import pandas as pd
    aapl = FoolStockNewsCrawler('aapl')
    aapl_list = aapl.get_transcripts_details()
    #print(aapl_list)
    df = pd.DataFrame(aapl_list)
    print(df)