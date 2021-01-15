import requests
import os
import credentials
import datetime as dt
from _datetime import timedelta

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": credentials.stock_api_key
}


# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def get_stock_price():
    now = dt.datetime.today()
    today = dt.datetime.today().strftime("%Y-%m-%d")
    yesterday = (now-timedelta(1)).strftime("%Y-%m-%d")
    result = requests.get(
        "https://www.alphavantage.co/query", params=stock_params)

    last_day_closing_price = float(result.json(
    )["Time Series (Daily)"][yesterday]["4. close"])
    today_opening_price = float(result.json(
    )["Time Series (Daily)"][today]["1. open"])
    # print(last_day_closing_price)
    return (last_day_closing_price, today_opening_price)


def detect_changes():
    last_day_closing_price, today_opening_price = get_stock_price()
    difference_in_closing_and_opennig = last_day_closing_price-today_opening_price
    # if difference_in_closing_and_opennig/last_day_closing_price
    print("difference is: %s" % (difference_in_closing_and_opennig))
    print("five percent is: %s" % (last_day_closing_price*0.05))
    if difference_in_closing_and_opennig < 0:
        print("Drop in the price by: %s" % (difference_in_closing_and_opennig))
        if difference_in_closing_and_opennig*(-1) >= last_day_closing_price*0.05:
            print("Significat drop")
    elif difference_in_closing_and_opennig > 0:
        print("Increase in price by: %s" % (difference_in_closing_and_opennig))
        if difference_in_closing_and_opennig >= last_day_closing_price*0.05:
            print("Significat growth")
    else:
        print("Nothing significant has happened")


# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

def main():
    detect_changes()


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
