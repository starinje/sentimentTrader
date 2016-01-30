#!/usr/bin/env

import time
import urllib2
import base64
import json
import sys
#from rest_client import getData
import datetime 
import ystockquote
from pprint import pprint



def calculate_day_index(start_date,stop_date): #need to return only trading days!!!
	delta = stop_date - start_date
	day_index = []
	for i in range(delta.days + 1):
		day_index.append(start_date + datetime.timedelta(days=i))
	return day_index


def calculate_sentiment_capture_window(day):
	#calculate and return 24 hour window block
	start_time = (day - datetime.timedelta(1)).replace(hour=16, minute=00, second=00)
	stop_time = day.replace(hour=16, minute=00)
	return start_time,stop_time

def calculate_content_sentiment():
	#insert code here that runs text through NLTK library and calculates a sentimant value
	
	
	return content_sentiment_value

#grab data for ticker_symbol from the data_source for the given period of time
def capture_relevant_data(day, data_source, ticker_symbol, start_time, stop_time): 


	counter = 0;
	total = 0;
	formatted_relevant_data = []
	formatted_relevant_data.append({"prediction date":day})
	stocktwits_data = file = open('./stocktwits_messages_2014-01-01-2014-12-31.json')
	
	#grab each tweet in data
	for line in stocktwits_data:
		counter = counter + 1
		total = total + 1
		id_counter = 0
		if(counter==5000):
			print "Processed " + str(total) + " lines."
			counter = 0

		line_json = json.loads(line)
		
		#check if tweet is the date rang
		timestamp = line_json['created_at']
		formatted_timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
		if start_time < formatted_timestamp < stop_time:

			#checks if there are symbols in the tweet
			if('symbols' in line_json.keys()):
				
				symbols = line_json['symbols']
				#loops through all of the symbols
				for symbol in symbols:
					symbol_instance = symbol['symbol']

	        		#checks if ticker is one of the symbols
		        	if(symbol_instance==ticker_symbol):
						if(line_json['entities'] is not None):
							if(line_json['entities']['sentiment'] is not None):
								if(line_json['entities']['sentiment']['basic'] is not None):
									#print "a sentiment has been found for: ", ticker_symbol
									relevant_data_instance = {}
									relevant_data_instance["id"] = line_json['id']
									relevant_data_instance["data_source"] = data_source
									relevant_data_instance["date_time_stamp"] = str(formatted_timestamp)
									relevant_data_instance["content"] = line_json['body']
									relevant_data_instance["bear_bull_tag"] = str(line_json['entities']['sentiment']['basic'])
									formatted_relevant_data.append(relevant_data_instance)
									id_counter = id_counter+1
									
		#breaks out of loop if data is past desired date
		if formatted_timestamp > stop_time:
			break
		
	return formatted_relevant_data
		


#assigns a sentiment for each individual data object in "relevant_data" object string. return an aggregated market_sentiment value (1-10)
def determine_market_sentiment(day, formatted_relevant_data):
	
	bearish_count = 0
	bullish_count = 0
	for data_point in formatted_relevant_data[1:]:

		if data_point["data_source"] == "stocktwits":
			#at first this will just be checking the bear/bull tag on a particular stocktwit
			#later will run text of stocktwit through text sentiment analysis function
			
			#eventually needs to be: (data_point["content"])
			sentiment_value = data_point["bear_bull_tag"]
			#eventually needs to be: (data_point["content"])
			if sentiment_value == "Bearish":
				bearish_count = bearish_count + 1
			if sentiment_value == "Bullish":
				bullish_count = bullish_count + 1

		if data_point["data_source"] == "twitter":
			print "need to figure out how to process twitter data"
			
			
	print "Bear Count: ", bearish_count
	print "Bull Count: ", bullish_count
	sentiment_volume = bearish_count + bullish_count
	market_sentiment = float(bearish_count)/float(bullish_count)
	print "Market Sentiment is: ", market_sentiment
	
	return market_sentiment, sentiment_volume
	
		
def determine_trade_recommendation(market_sentiment):
	#return "buy", "sell", or "hold"
	#market_sentiment will be a value between 1 and 10, so we need to determine the thresholds for market sentiment
	if market_sentiment < .3:
		trade_action  = "sell"
		
	elif market_sentiment > .4:
		trade_action = "buy"
		
	else:
		trade_action = "hold"
		
		
	return trade_action


def open_position(day, cash_value, ticker_symbol):
	#execute trade based on trade_decision
	#open up connection with exchange service - bitreserve maybe?
	buy_price = get_price(day, ticker_symbol)
	print "buy price is: ", buy_price
	position_quantity = float(cash_value)/float(buy_price) 
	position_value = float(buy_price)*position_quantity
	leftover_cash  = float(cash_value) - float(position_value)
	return position_value, position_quantity, leftover_cash
 
def close_position(day, position_quantity,ticker_symbol):
	#calculate transaction fee and incorporate into close_position_value
	buy_price = get_price(day, ticker_symbol)
	close_position_value = float(buy_price)*position_quantity
	return close_position_value


def calculate_position_value(day, quantity, ticker_symbol):
	position_value = get_price(day, ticker_symbol)*quantity
	return position_value
	
	
def get_price(day, ticker_symbol):
	
	date_string = str(day)
	date = date_string[:10]
	
	#data = ystockquote.get_historical_prices(ticker_symbol, date, date)
	
	#close_price =  data[date]['Close']
	close_price = 230
	return close_price
	
	
def calculate_content_sentiment(text):
	
	#runs text through sentiment analysis engine
	
	return content_sentiment
	
def calculate_market_sentiment(start_time, stop_time, ticker, data_feed_source):
	
	#opens up database
	#look up all entries that match the date, ticker symbol, and data_feed_source
	#run all of these entries through a calculate_sentiment() function	
	#returns net sentiment for the market for that time period 
	
	return market_sentiment
	
	
def execute_trading_strategy(data_sources, ticker_symbol, day, cash_value, equities_position, position_value, position_quantity, close_position_value):
	

	trade_action = "hold"

	#creates two item list with timestamps bookends for gathering sentiment
	start_time, stop_time = calculate_sentiment_capture_window(day)
	
	#opens up database
	#look up all entries that match the date, ticker symbol, and data_feed_source
	#run all of these entries through a calculate sentiment() function
	market_sentiment = calculate_market_sentiment(start_time, stop_time, ticker, data_feed_source)
	
	#determines trade action based on bear/bull ratio
	trade_recommendation = determine_trade_recommendation(market_sentiment)
		
	if equities_position == 0:
		if trade_recommendation == "buy":
			print "trade_action is buy"
			print "buying stock"
			position_value, position_quantity, leftover_cash = open_position(day, cash_value,ticker_symbol)
			cash_value = leftover_cash 
			portfolio_value = position_value + cash_value	
			print "cash value is: ", cash_value
			print "position value is: ", position_value
			print "porfolio value is: ", portfolio_value
			trade_action = "buy"
			equities_position = 1
				
		elif trade_recommendation == "sell":
			trade_action = "hold"
			print "trade_action is sell"
			print "but nothing to sell :("
			portfolio_value = cash_value
			print "cash value is: ", cash_value
			print "position value is: ", position_value
			print "porfolio value is: ", portfolio_value
				
		elif trade_recommendation == "hold":
			trade_action = "hold"
			print "trade_action is hold"
			print "but no positions"
			portfolio_value = cash_value
			print "cash value is: ", cash_value
			print "position value is: ", position_value
			print "porfolio value is: ", portfolio_value				
				
	elif equities_position == 1:
		
		if trade_recommendation == "buy":
			trade_action = "hold"
			print "trade_action is buy"
			print "but nothing to buy :("
			portfolio_value = position_value + cash_value
			print "cash value is: ", cash_value
			print "position value is: ", position_value
			print "porfolio value is: ", portfolio_value
				
		elif trade_recommendation == "sell":
			trade_action = "sell"
			print "trade_action is sell"
			print "selling stock"
			close_position_value = close_position(day, position_quantity, ticker_symbol)
			print "close position value is: ", close_position_value
			cash_value = cash_value + close_position_value
			position_value =  0
			portfolio_value = cash_value
			print "cash value is: ", cash_value
			print "position value is: ", position_value
			print "porfolio value is: ", portfolio_value
			equities_position = 0
				
		elif trade_recommendation == "hold":
			trade_action = "hold"
			print "trade_action is hold"
			print "holding stock"
			portfolio_value = position_value + cash_value
			print "cash value is: ", cash_value
			print "position value is: ", position_value
			print "porfolio value is: ", portfolio_value
				
	return portfolio_value, cash_value, equities_position, position_value, position_quantity, close_position_value, trade_action, market_sentiment, sentiment_volume

def append_to_graph_data(graph_data, day, portfolio_value, close_price, trade_action, market_sentiment, sentiment_volume):

	day_data = {}
	day_data["date"] = str(day)
	day_data['portfolio_value'] = portfolio_value
	day_data['close_price'] = close_price
	day_data['trade_action'] = trade_action
	day_data['market_sentiment'] = market_sentiment
	day_data['sentiment_volume'] = sentiment_volume
	
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
data_sources = {"stocktwits"}
start_date = datetime.datetime(2014, 1, 02, 00, 0, 0, 0)  #year, month, day - need to indicate minute and second 
stop_date = datetime.datetime(2014, 2 , 20, 00, 0, 0, 0) #year, month, day



#create list of days to analyse from date range
day_index = calculate_day_index(start_date,stop_date)	

#list to hold graphing data, keeping track of portfolio value
graph_data = [] 

#loop through every day and run algorithm, keeping 
for day in day_index:
	
	date_string = str(day)
	date = date_string[:10]
	data = 1 #ystockquote.get_historical_prices(ticker_symbol, date, date)

	if data: #if data is returned then it is a trading day
		print "processing day: ", day
		portfolio_value, cash_value, equities_position, position_value, position_quantity, close_position_value, trade_action, market_sentiment, sentiment_volume = execute_trading_strategy(data_sources, ticker_symbol, day, cash_value, equities_position, position_value, position_quantity, close_position_value)
		close_price = get_price(day, ticker_symbol)
		print "close price is: ", close_price
		print "market sentiment is: ", market_sentiment
		print "sentiment volume is: ", sentiment_volume
		print "\n"
		graph_data = append_to_graph_data(graph_data, day, portfolio_value, close_price, trade_action, market_sentiment, sentiment_volume)
		time.sleep(1)
	
		print graph_data
		dict_to_json(graph_data)
		print "\n"
		
	if not data:
		print "not a trading day"
