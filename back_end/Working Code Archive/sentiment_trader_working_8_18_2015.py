#!/usr/bin/env

import time
import urllib2
import base64
import json
import sys
#from rest_client import getData
from datetime import date, timedelta as td
from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info(bar.getClose())

def calculate_day_index(start_date,stop_date): #only trading days!!!
	delta = stop_date - start_date
	day_index = []
	for i in range(delta.days + 1):
		day_index.append(start_date + td(days=i))
	return day_index


def calculate_sentiment_capture_window(day):
	#do we want to capture all twitter for the last 24 hours or just live trading times?
	start_time = "x"
	stop_time = "y"
	return start_time,stop_time


#read in twitter feed on a particular hashtag
def capture_twitter_data(ticker_symbol, start_time, stop_time): #in day minutes seconds format
	#capture twitter data for ticker_symbol for the given period of time
	#format data and store in database
	
	twitter_data = ["good_stuff", "bad_stuff", "good_stuff", "good_stuff", "good_stuff", "bad_stuff", "bad_stuff", "good_stuff", "bad_stuff","good_stuff"]
	return twitter_data


def determine_sentiment(twitter_data):
	#iterate over all tweets and assign each one a sentiment value. Perhaps using nltk or some other speech processing library
	#take average of all moods to determine overall mood for entire data set. (negative, neutral, positive)
	# if mood falls in certain ranges than set trade_decision to (buy, sell, hold)
	#how far ahead are we predicting?
	if twitter_data == "bad_stuff":
		print "bad stuff detected"
		sentiment = "bad"
		
	elif twitter_data == "good_stuff":
		print "good stuff detected"
		sentiment = "good"
	elif  twitter_data  == "neutral_stuff":
		print "neutral stuff detected"
		sentiment = "neutral"
	return sentiment
	
	
def determine_trade_action(sentiment):
	#return "buy", "sell", or "hold"
	if sentiment == "bad":
		trade_action  = "sell"
	elif sentiment == "good":
		trade_action = "buy"
	elif sentiment == "neutral":
		trade_action = "hold"
	return trade_action


def open_position(cash_value, ticker_symbol):
	#execute trade based on trade_decision
	#open up connection with exchange service - bitreserve maybe?
	buy_price = get_price(ticker_symbol)
	position_quantity = cash_value/buy_price 
	position_value = buy_price*position_quantity
	leftover_cash  = cash_value - position_value
	return position_value, position_quantity, leftover_cash
 
def close_position(position_quantity,ticker_symbol):
	#calculate transaction fee and incorporate into close_position_value
	buy_price = get_price(ticker_symbol)
	close_position_value = buy_price*position_quantity
	return close_position_value


def calculate_position_value(quantity, ticker_symbol):
	position_value = get_price(ticker_symbol)*quantity
	return position_value
	
	
def get_price(ticker_symbol):
	price =  230
	return price
	
	
def execute_trading_strategy(day, cash_value, equities_position, position_value, position_quantity, close_position_value,i):

	start_time, stop_time = calculate_sentiment_capture_window(day) #creates two item list with timestamps bookends for gathering sentiment
	twitter_data = capture_twitter_data(ticker_symbol, start_time, stop_time)
	sentiment = determine_sentiment(twitter_data[i])

	trade_action = determine_trade_action(sentiment)
		
	if equities_position == 0:
		if trade_action == "buy":
			print "trade_action is buy"
			print "buying stock"
			position_value, position_quantity, leftover_cash = open_position(cash_value,ticker_symbol)
			cash_value = leftover_cash 
			portfolio_value = position_value + cash_value	
			print "cash value is: ", cash_value
			print "position value is: ", position_value
			print "porfolio value is: ", portfolio_value
			equities_position = 1
				
		elif trade_action == "sell":
			print "trade_action is sell"
			print "but nothing to sell :("
			portfolio_value = cash_value
			print "cash value is: ", cash_value
			print "position value is: ", position_value
			print "porfolio value is: ", portfolio_value
				
		elif trade_action == "hold":
			print "trade_action is hold"
			print "but no positions"
			portfolio_value = cash_value
			print "cash value is: ", cash_value
			print "position value is: ", position_value
			print "porfolio value is: ", portfolio_value				
				
	elif equities_position == 1:
		
		if trade_action == "buy":
			print "trade_action is buy"
			print "but nothing to buy :("
			portfolio_value = position_value + cash_value
			print "cash value is: ", cash_value
			print "position value is: ", position_value
			print "porfolio value is: ", portfolio_value
				
		elif trade_action == "sell":
			print "trade_action is sell"
			print "selling stock"
			close_position_value = close_position(position_quantity, ticker_symbol)
			print "close position value is: ", close_position_value
			cash_value = cash_value + close_position_value
			position_value =  0
			portfolio_value = cash_value
			print "cash value is: ", cash_value
			print "position value is: ", position_value
			print "porfolio value is: ", portfolio_value
			equities_position = 0
				
		elif trade_action == "hold":
			print "trade_action is hold"
			print "holding stock"
			portfolio_value = position_value + cash_value
			print "cash value is: ", cash_value
			print "position value is: ", position_value
			print "porfolio value is: ", portfolio_value
				
	return portfolio_value, cash_value, equities_position, position_value, position_quantity, close_position_value, trade_action, i

def append_to_graph_data(graph_data, day, portfolio_value, close_price, trade_action):

	day_data = {}
	day_data["date"] = str(day)
	day_data['portfolio_value'] = portfolio_value
	day_data['close_price'] = close_price
	day_data['trade_action'] = trade_action
	
	graph_data.append(day_data)



	return graph_data
	
def dict_to_json(dict_data):
	with open('../front_end/output.json', 'w') as fp:
	    	json.dump(graph_data, fp)
	return 
	






#main 
cash_value = 10000 
equities_position = 0 
position_value = 0
position_quantity = 0
close_position_value = 0
ticker_symbol = "TSLA"
start_date = date(2011, 10, 10) #year, month, day - need to indicate minute and second 
stop_date = date(2013, 12, 12) #year, month, day

#create list of days to analyse from date range
day_index = calculate_day_index(start_date,stop_date)	
graph_data = [] #list to hold graphing data

i = 0
for day in day_index:
	if i < 9 :
		print "i's value is: ", i
		i = i + 1
		print "The day is: ", day
		portfolio_value, cash_value, equities_position, position_value, position_quantity, close_position_value, trade_action, i = execute_trading_strategy(day, cash_value, equities_position, position_value, position_quantity, close_position_value, i)
		close_price = get_price(ticker_symbol)
		print "\n"
		graph_data = append_to_graph_data(graph_data, day, portfolio_value, close_price, trade_action)
		#time.sleep(1)
	
		
print graph_data
dict_to_json(graph_data)
print "\n"

# Load the yahoo feed from the CSV file
#feed = yahoofeed.Feed()
#feed.addBarsFromCSV("tsla", "orcl-2000.csv")

# Evaluate the strategy with the feed's bars.
#myStrategy = MyStrategy(feed, "tsla")
#myStrategy.run()
		