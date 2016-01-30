#!/usr/bin/env

import ystockquote
from pprint import pprint

date = '2013-01-03'
data = ystockquote.get_historical_prices('GOOGL', date, date)
print data[date]['Close']



