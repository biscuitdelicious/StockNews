import requests
import datetime as dt
from twilio.rest import Client
import os


STOCK = "TSLA"
API_KEY = os.environ.get('API_KEY')
NEWS_KEY = os.environ.get('NEWS_KEY')
account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')
client = Client(account_sid, auth_token)

YOUR_PHONE_NUMBER = ''
FROM_PHONE_NUMBER = ''

stock_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=TSLA&apikey=YOUR_API_KEY'
news_url = 'https://newsapi.org/v2/everything?q=tesla&apiKey=YOUR_API_KEY'


def percentage(part, whole):
    if whole == 0:
        return 0
    else:
        return 100 * float(part)/float(whole)


response_stock = requests.get(url=stock_url)
response_stock.raise_for_status()

response_news = requests.get(url=news_url)
response_news.raise_for_status()

ytday = dt.datetime.now() - dt.timedelta(1)
the_day_before_ytday = dt.datetime.now() - dt.timedelta(2)
yesterday = ytday.strftime('%Y-%m-%d')
the_day_before_yesterday = the_day_before_ytday.strftime('%Y-%m-%d')

stock_data = response_stock.json()
news_data = response_news.json()
yesterday_price = 0
the_day_before_yesterday_price = 0

for (date, dateum) in stock_data['Time Series (Daily)'].items():
    if date == the_day_before_yesterday:
        the_day_before_yesterday_price = dateum['4. close']
    if date == yesterday:
        yesterday_price = dateum['4. close']

if yesterday_price == 0 or the_day_before_yesterday_price:
    try:
        raise KeyError('Invalid range or one of the days is in weekend.')
    finally:
        pass


difference = float(the_day_before_yesterday_price) - float(yesterday_price)
percent = percentage(round(difference, 2), the_day_before_yesterday_price)

i = 0
if percent > 5 or percent < -5:
    for article in news_data['articles']:
        while i < 3:
            message = client.messages.create(
                body=article['description'],
                from_=FROM_PHONE_NUMBER,
                to=YOUR_PHONE_NUMBER
                )
            break
        i = i + 1


# I FINALLY DID IT LET'S FUCKING GO