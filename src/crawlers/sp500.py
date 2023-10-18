import requests
from bs4 import BeautifulSoup

import pandas as pd

def get_sp500():
    # get the response in the form of html
    url="https://www.liberatedstocktrader.com/sp-500-companies-list-by-sector-market-cap/"
    # table_class="sortable wikitable jquery-tablesorter"
    response=requests.get(url)
    print(response.status_code)
    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    largest_company_table = soup.find('table',{'style':"border-collapse: collapse;"})
    df = pd.read_html(str(largest_company_table))[0]
    headers = df.iloc[0]
    df = pd.DataFrame(df.values[1:], columns=headers)
    df.columns = [col.lower() for col in df.columns]
    return dfls
