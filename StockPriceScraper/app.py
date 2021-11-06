

# importing all the required modules

import pandas as pd
from bs4 import BeautifulSoup
from requests.api import head
import spacy
import requests
import streamlit as st
from datetime import date
import yfinance as yf


st.write(f'Buzzing Stocks on {date.today()} :zap: ')
nlp = spacy.load('en_core_web_sm')

def extract_data_from_links(rsslink: str):
    headings = []
    # get url response
    response = requests.get(rsslink)
    soup = BeautifulSoup(response.content, features='html.parser')
    headings = soup.findAll('title')
    return headings
    
def generate_stock_info(headings):

    stock_info_dict = {
        'org_name': [],
        'symbol': [],
        'current_price': [],
        'day_high': [],
        'day_low': [],
        'forward_pe': [],
    }

    stocks_df = pd.read_csv('./data/ind_nifty500list.csv')
    for title in headings:
        doc = nlp(title.text)
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                try:
                    if stocks_df['Company Name'].str.contains(ent.text).sum():
                        symbol =  stocks_df[stocks_df['Company Name'].str.contains(ent.text)]['Symbol'].values[0]
                        org_name =  stocks_df[stocks_df['Company Name'].str.contains(ent.text)]['Company Name'].values[0]
                        
                        stock_info = yf.Ticker(symbol+".NS").info
                        print('**')
                        print(stock_info.keys())
                        print('**')
                        stock_info_dict['org_name'].append(org_name)
                        stock_info_dict['symbol'].append(symbol)
                        stock_info_dict['current_price'].append(stock_info['currentPrice'])
                        stock_info_dict['day_high'].append(stock_info['dayHigh'])
                        stock_info_dict['day_low'].append(stock_info['dayLow'])
                        stock_info_dict['forward_pe'].append(stock_info['forwardPE'])
                    else:
                        pass
                except:
                    pass

    print('----------')
    print(stock_info_dict)
    print('----------')
    df = pd.DataFrame(stock_info_dict)
    return df



user_input = st.text_input('Add any RSS link here', 'https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms')
headings = extract_data_from_links(user_input)
stock_info_df = generate_stock_info(headings)
stock_info_df.drop_duplicates(inplace=True)
st.dataframe(stock_info_df)
