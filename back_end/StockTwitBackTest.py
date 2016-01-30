#!/usr/bin/env
import json

file = open('./stocktwits_messages_2014-01-01-2014-12-31.json')

counter = 0;
total = 0;
results = {}

for line in file:
    counter = counter + 1
    total = total + 1
    if(counter==5000):
        print "Processed " + str(total) + " lines."
        counter = 0
    line1 = json.loads(line)

    if('symbols' in line1.keys()):
        symbols = line1['symbols']
        print symbols
        symbol = symbols[0]['symbol']

        if(symbol=='TSLA'):
            print line
            date = line1['created_at'][:10]
            sentiment = ''
            if(line1['entities'] is not None):
                if(line1['entities']['sentiment'] is not None):
                    if(line1['entities']['sentiment']['basic'] is not None):
                        sentiment = line1['entities']['sentiment']['basic']

            if(sentiment is None):
                continue
            else:
                if(date in results.keys()):
                    dateVal = results[date]

                    if(sentiment in dateVal.keys()):
                        sentimentVal = dateVal[sentiment]
                        sentimentVal = sentimentVal + 1
                        dateVal[sentiment]=sentimentVal
                    else:
                        dateVal[sentiment] = 1

                    results[date]=dateVal
                else:
                    dateVal = {}
                    dateVal[sentiment]=1
                    results[date]=dateVal

#write results to file
print "Writing to file."
outputFile = open("APPL.txt","w")

for date in results.keys():
    data = results[date]
    bears=0
    bulls=0

    if('Bullish' in data.keys()):
        bulls = data['Bullish']
    if('Bearish' in data.keys()):
        bears = data['Bearish']

    outputFile.write(str(date) + "," + str(bulls) + "," + str(bears) + "," + "\n")
