"""
App factory for our flask service
"""
import logging

from flask import Flask

app = Flask(__name__)

@app.route('/data')
def get_data():
    from craigslist_scrapper import CraigslistScrapper
    c = CraigslistScrapper()
    data = c.parse_listings().dropna(subset=['price']).to_json(orient='records')
    return data

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(filename)s] [%(funcName)s] [%(levelname)s] %(message)s')
    app.run(host='127.0.0.1', debug=False, port=5000, use_reloader=False)