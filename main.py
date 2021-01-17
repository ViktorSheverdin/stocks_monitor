import requests
import os
import credentials
import datetime as dt
from _datetime import timedelta
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": credentials.stock_api_key
}

news_params = {
    "apikey": credentials.news_api_key,
    "q": COMPANY_NAME
}

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").


def get_stock_price():
    now = dt.datetime.today()
    # today = dt.datetime.today().strftime("%Y-%m-%d")
    # yesterday = (now-timedelta(1)).strftime("%Y-%m-%d")
    today = "2021-01-14"
    yesterday = "2021-01-13"
    result = requests.get(
        "https://www.alphavantage.co/query", params=stock_params)

    print(result.json()["Time Series (Daily)"][yesterday])

    last_day_closing_price = float(result.json(
    )["Time Series (Daily)"][yesterday]["4. close"])
    today_opening_price = float(result.json(
    )["Time Series (Daily)"][today]["1. open"])
    return (last_day_closing_price, today_opening_price)


def detect_changes():
    last_day_closing_price, today_opening_price = get_stock_price()
    difference_in_closing_and_opennig = last_day_closing_price-today_opening_price
    if difference_in_closing_and_opennig < 0:
        if difference_in_closing_and_opennig*(-1) >= last_day_closing_price*0.05:
            print("Significat drop")
    elif difference_in_closing_and_opennig > 0:
        if difference_in_closing_and_opennig >= last_day_closing_price*0.05:
            print("Significat growth")
    else:
        print("Nothing significant has happened")
    return float(difference_in_closing_and_opennig/last_day_closing_price)


# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

def find_news():
    result = requests.get(
        "https://newsapi.org/v2/everything", params=news_params)
    title = (result.json()["articles"][0]["title"])
    description = (result.json()["articles"][0]["description"])
    url_to_article = (result.json()["articles"][0]["urlToImage"])
    return (title, description, url_to_article)

# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


def send_text(body_of_message):
    client = Client(credentials.twilo_account_sid,
                    credentials.twilo_auth_token)

    message = client.messages.create(
        body=body_of_message,
        from_=credentials.twilo_phone_num,
        to=credentials.my_phone_num
    )
    print(message.status)


def main():
    percentage_difference = detect_changes()
    title, description, url_to_article = find_news()
    print(title)
    print(description)
    print(url_to_article)
    body_of_message = """    
\n
%s: %.2f
Headline: %s
Brief: %s
URL: %s
    
    """ % (STOCK, percentage_difference,
           title, description, url_to_article)
    print(body_of_message)


main()


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
