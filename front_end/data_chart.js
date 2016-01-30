var chart = AmCharts.makeChart( "chartdiv", {
  type: "stock",
  "theme": "light",  

  dataSets: [ {
      fieldMappings: [ {
        fromField: "portfolio_value",
        toField: "portfolio_value"
      }, {
        fromField: "trade_action",
        toField: "trade_action"
      }, {
        fromField: "close_price",
        toField: "close_price"
      },{
        fromField: "market_sentiment",
        toField: "market_sentiment"
      },{
        fromField: "sentiment_volume",
        toField: "sentiment_volume"
      }],
      
      //dataProvider: chartData,
      categoryField: "date",
      
      //stockEvents: stockEvents_data
    } ],
  
  panels: 
  [ 
    //first graph
    {
        showCategoryAxis: false,
        title: "Close Price",
        percentHeight: 25,
  
        stockGraphs: [ 
          {
          id: "g1",
          valueField: "close_price",
        } 
                      ],
        stockLegend: {
          valueTextRegular: " ",
          markerType: "none"
        }
    },

   //second graph
    {
        title: "Portfolio Value",
        percentHeight: 25,
        stockGraphs: [ {
          id: "g2",
          valueField: "portfolio_value",
          type: "column",
          showBalloon: false,
          fillAlphas: 1
          } ],

      stockLegend: {
        periodValueTextRegular: "[[value.close]]"
      }
    },
    
    {
        title: "Market Sentiment",
        percentHeight: 25,
        stockGraphs: [ {
          id: "g3",
          valueField: "market_sentiment",
          type: "column",
          showBalloon: false,
          fillAlphas: 1
          } ],

      stockLegend: {
        periodValueTextRegular: "[[value.close]]"
      }
    },
        {
        title: "Sentiment Volume",
        percentHeight: 25,
        stockGraphs: [ {
          id: "g4",
          valueField: "sentiment_volume",
          type: "column",
          showBalloon: false,
          fillAlphas: 1
          } ],

      stockLegend: {
        periodValueTextRegular: "[[value.close]]"
      }
    }
    

  ],

  chartScrollbarSettings: {
    graph: "g1"
  },

   chartCursorSettings: {
    valueBalloonsEnabled: true,
    graphBulletSize: 1,
    valueLineBalloonEnabled: true,
    valueLineEnabled: true,
    valueLineAlpha: 0.5
  },

  periodSelector: {
    periods: [ {
      period: "DD",
      count: 10,
      label: "10 days"
    }, {
      period: "MM",
      count: 1,
      label: "1 month"
    }, {
      period: "YYYY",
      count: 1,
      label: "1 year"
    }, {
      period: "YTD",
      label: "YTD"
    }, {
      period: "MAX",
      label: "MAX"
    } ]
  },

  panelsSettings: {
    usePrefixes: true
  },

  "export": {
    "enabled": true
  }

});


function ResetGraphData(chart) {
	var file_new = "./output.json";
	
	$.getJSON(file_new, function(data_new) {
      	  
	    var stock_events_data = [];
	    
	    for (day in data_new) {
	      
          var stock_event = {}
        	stock_event["date"] = new Date (data_new[day].date)
        	
        	if (data_new[day].trade_action == "sell"){
        	  stock_event['backgroundColor'] = "#ED1B24"
        	}
        	
        	if (data_new[day].trade_action == "buy"){
        	  stock_event['backgroundColor'] = "#85CDE6"
        	}
        	
        	stock_event['type'] = "text"
        	stock_event['text'] = data_new[day].trade_action
        	stock_event['graph'] = "g1"
        	stock_event['description'] = "This is description of an event"
        	
        	stock_events_data.push(stock_event);
      }
	  
	    console.log(stock_events_data)
	    console.log(chart.dataSets)
      chart.dataSets[0].stockEvents = stock_events_data;
	    chart.dataSets[0].dataProvider = data_new; 

 		  chart.validateData();
	});
	
}


