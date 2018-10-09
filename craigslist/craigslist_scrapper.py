"""
Retrieve data from craigslist:
https://newyork.craigslist.org/d/video-gaming/search/vga
"""

import time
import logging

import bs4
import pandas as pd
import requests

class CraigslistScrapper():
    def __init__(self, base_url=None, keywords=None):
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = 'https://newyork.craigslist.org/search/vga'
        if keywords:
            self.keywords = keywords
        else:
            self.keywords = ('xbox', 'playstation', 'nintendo')
        logging.debug('Using url=[{}] with keywords=[{}]'.format(self.base_url, self.keywords))
        self.areas = self._init_areas()
        
    def _init_areas(self):
        raw_data = requests.get(self.base_url)
        bs_data = bs4.BeautifulSoup(raw_data.text, features="html.parser")
        res = {}
        for bs_item in bs_data.find_all('select', id='areaAbb'):
            sub_items = bs_item.find_all('option')
            for sub_item in sub_items:
                res[sub_item.text] = sub_item.get('value')
        return res

    def parse_listings(self, area=None, limit=1):
        """

        """
        if area:
            raw_datas = [(area, requests.get(self.base_url.replace('newyork', area)))]
        else:
            raw_datas = []
            for area in self.areas.values():
                raw_datas.append((area, requests.get(self.base_url.replace('newyork', area))))
        res = []
        for area, resp in raw_datas:
            bs_data = bs4.BeautifulSoup(resp.text, features="html.parser")
            listings = bs_data.find_all('li', class_='result-row')
            logging.debug('Retrieving area=[{}] #listings={}'.format(area, len(listings)))
            for bs_item in listings:
                if bs_item.find(class_='result-price'):
                    price = bs_item.find(class_='result-price').text
                    price = float(price.replace('$', ''))
                else:
                    price = pd.np.nan
                title = bs_item.find(class_='result-title').text
                url = bs_item.find(class_='result-title').get('href')
                res.append((title, price, url, area))
        return pd.DataFrame(res, columns=['title', 'price', 'url', 'area'])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(filename)s] [%(funcName)s] [%(levelname)s] %(message)s')
    c = CraigslistScrapper()
    df = c.parse_listings().dropna(subset=['price']).to_json(orient='records')
    print(df)