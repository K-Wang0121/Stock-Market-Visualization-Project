#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 20:33:13 2022

@author: kevin
"""



# Python Stock Market Visualization Project

# Goal: To determine the top stock in the Airline industry to invest for the year 2016(by analyzing data of the stock market before 2016), based on the following success criterias: the firm's financial performance and its return rate on investment.
# 
# To compare the airline companies' financial performance, we'll calculate their cash ratio and current ratio.
# 
# On the other hand, to compare the return rate on investment of the firms in the airline industry, we'll calculate the volatility and relative price strength of their stock prices. 




import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_option_menu import option_menu
pd.options.plotting.backend = "plotly" 

fundamentals = pd.read_csv('fundamentals.csv')
prices = pd.read_csv('prices.csv')
securities = pd.read_csv('securities.csv')
combined = fundamentals.merge(securities, on='ticker_symbol').copy()
combined = combined[combined['period_ending'] == '2015-12-31']
airlines = combined[combined['gics_sub_industry'] == 'Airlines'].copy()
airlines_2015 = airlines[airlines['period_ending'] == '2015-12-31']

AAL_prices = prices[prices['symbol'] == 'AAL']
ALK_prices = prices[prices['symbol'] == 'ALK']
DAL_prices = prices[prices['symbol'] == 'DAL']
LUV_prices = prices[prices['symbol'] == 'LUV']
UAL_prices = prices[prices['symbol'] == 'UAL']
all_prices = pd.concat([AAL_prices, ALK_prices, DAL_prices, LUV_prices, UAL_prices])
all_prices.rename(columns={'low':'low (USD)', 'high':'high (USD)'})
all_prices = all_prices[all_prices['date'].str.contains(r'201[012345]-\d+-\d+')]


st.set_page_config(layout="wide")
with st.sidebar: 
	selected = option_menu(
		menu_title = 'Navigation Pane',
		options = ['Abstract', 'Background Information', 'Data Cleaning', 
		'Exploratory Analysis','Data Analysis', 'Conclusion', 'Bibliography'],
		menu_icon = 'menu-up',
		icons = ['bookmark-check', 'book', 'clipboard2-check', 'map', 'boxes', 'bar-chart', 
		'check2-circle','blockquote-left'],
		default_index = 0
		)



if selected == 'Abstract':
	
    st.title('Abstract')
    st.image("Trading Floor.png", caption='A typical working scenario on the trading floor. Source: https://i-itm.com/5-things-to-know-before-the-stock-market-opens-wednesday/')
                   
    st.markdown('As stock markets around the world continues to expand, undoubtfully that great quantities of investors got themselves involved in the business, ranging from hedge funds to individual stock traders. In this case study, we\'re going to analyze airline stocks based on two aspects: financial performance and return on investment, namely evaluating the firms\' cash ratio, current ratio, as well as the volatility and relative price strength of their stocks\' market performance. At the end of this case study, we\'ll come to a conclusion of the top stock to invest in for the year 2016 in the U.S S&P 500 index.')
    st.markdown('')
    st.markdown('')
    st.markdown('')
    st.markdown('')
    st.caption('Author: Kevin Yuxin Wang')


if selected == 'Background Information':
    
    st.title('Background Information')
    st.header('What is Stock Trading?')
    st.caption('The following is extraced from Investopedia, a financial media website that is founded in 1999, and headquartered in New York City. Source: https://www.investopedia.com/articles/investing/082614/how-stock-market-works.asp')
    st.markdown('A stock is a financial instrument that represents ownership in a company or corporation and represents a proportionate claim on its assets (what it owns) and earnings (what it generates in profits). Stocks are also called shares or equity.')
    st.markdown('Owning stock means that a shareholder owns a slice of the company equal to the number of shares held as a proportion of the company\'s total outstanding shares. For instance, an individual or entity that owns 100,000 shares of a company with one million outstanding shares would have a 10% ownership stake in it. Most companies have outstanding shares that run into the millions or billions.')
    st.header('Key Takeaways')
    st.markdown('- Stocks represent ownership equity in the firm and give shareholders voting rights as well as a residual claim on corporate earnings in the form of capital gains and dividends.')          
    st.markdown('- Individual and institutional investors come together on stock exchanges to buy and sell shares in a public venue.')
    st.markdown('- Share prices are set by supply and demand as buyers and sellers place orders.')
    st.markdown('- Order flow and bid-ask spreads are often maintained by specialists or market makers to ensure an orderly and fair market.')
    st.markdown('- Listing on exchanges may provide companies with liquidity and the ability to raise capital but it can also mean higher costs and increased regulation.')
          
    
    st.header('Original Datasets')
    st.subheader('Context')
    st.markdown('The three datasets that is going to be analyzed in this stock market case study is: \'fundamentals.csv\', \'prices.csv\', and \'securities.csv\', which are all collected from https://www.kaggle.com/datasets/dgawlik/nyse. Furthermore, the datasets as mentioned previously consists of fundamental data of the S&P 500 companies, along with their historical prices on the stock market.')
    st.markdown('Specifically, the \'prices.csv\' dataset mainly consists of daily trading information spanning from 2010 - 2016 for the majority of the firms, as shown below:')
    st.caption('Click on the expand key to zoom in')
    st.write(prices)
    
    st.markdown('On the other hand, the \'fundamentals.csv\' dataset consists of metrics extracted from the annual SEC 10k fillings(2012-2016), which is adequate to perform analysis on key investment indicators(e.g current ratio). Subsequently, the \'securities.csv\' dataset is supplementry to the \'fundamentals.csv\' dataset, consisting of qualitative data(general descriptions of each company, e.g industry).')
    st.markdown('\'fundamentals.csv\'')
    st.caption('Click on the expand key to zoom in')
    st.write(fundamentals)
    st.markdown('\securities.csv\'')
    st.caption('Click on the expand key to zoom in')
    st.write(securities)
    
    
    
if selected == 'Data Cleaning':
    
    st.title('Data Cleaning')
    st.header('First Dataset')
    st.markdown('To start off our data cleaning process, we will remove unnecessary elements in the column title of the \'fundamentals.csv\' dataset.')
    st.code('cleaned_columns = [column.replace(\'\'\', \'\').replace(\'.\', \'\').replace(\' \', \'_\').replace(\'-\', \'_\').replace(\'/\', \'_\').lower() for column in fundamentals.columns]', language="python")
    fundamentals.columns = cleaned_columns
    st.markdown('Merge \'fundamentals.csv\' with \'securities.csv\', to enrich the string values in the \'fundamentals.csv\' dataset, specifically the qualitative data of each firm(E.g. industry).')
    st.code('combined = fundamentals.merge(securities, on=\'ticker_symbol\')', language='Python')
    st.markdown('As accordingly to the investigation purpose of this case study, we are trying to reach an accurate conclusion for the top airline stock to invest in for the year 2016, so we should filter out companies in the \"Airlines\" industry.')
    st.code('airlines = combined[combined[\'gics_sub_industry\'] == \'Airlines\'].copy()', language='Python')
    st.markdown('From the table above, we can deduce that in our merged dataset \'combined\',in total there are 5 firms present. Represented by their ticker symbol: #\'AAL\', \'ALK\', \'DAL\', \'LUV\', and \'UAL\'. Since in this Python Visualization project we are focusing on data that is representative of statistics from the year 2015 and before, the next step in our agenda will be filtering rows where the \'period_ending\' column equals \'2015-12-31\'.')
    st.code('airlines_2015 = airlines[airlines[\'period_ending\'] == \'2015-12-31\']', language='Python')
    st.markdown('Note: the \'airlines_2015\' dataset will be used to evaluate the financial performance of the airline stocks, namely their cash ratio and current ratio.')
    st.caption('Click on the expand key to zoom in')
    st.write(airlines_2015)
    
    st.header('Second Dataset')
    st.markdown('To ensure the clarity of the column labels of the \'all_prices.csv\' dataset, we should add the corresponding measurement unit(USD) for the \'low\' and \'high\' columns.')
    st.code('all_prices.rename(columns={\'low\':\'low (USD)\', \'high\':\'high (USD)\'})', language='Python')
    st.markdown('Since we\'re providing a foresight of the top stocks to invest in for the year 2016, we should remove data from \'2016-00-00\' onwards to ensure the accuracy of the analysis.')
    st.code('all_prices = all_prices[all_prices[\'date\'].str.contains(r\'201[012345]-\d+-\d+\')]', language='Python')
    st.markdown('Note: the \'all_prices\' dataset will be used to evaluate the return on investment of the airline stocks, namely the volatility and relative price strength of their stock prices.')
    st.caption('Click on the expand key to zoom in')
    st.write(all_prices)



if selected == 'Exploratory Analysis':
    
	st.title('Exploratory Analysis')
    st.subheader('With Pandas Profiling')
    profile1 = ProfileReport(airlines_2015)
	st_profile_report(profile1)
    
    profile2=ProfileReport(all_prices)
    st_profile_report(profile2)
    

    
    
if selected == 'Data Analysis':
    st.title('Data Analysis')
    st.header('Financial Performance')
    st.subheader('Factor 1: Cash Ratio')
    st.markdown('According to Investopia: \"(A high cash ratio)This means a company has more cash on hand, lower short-term liabilities, or a combination of the two. It also means a company will have greater ability to pay off current debts as they come due.\" Resultingly, a firm\'s performance and it\'s cash ratio stands in a positive relationship. In other words, the two variables(\'a firm\'s performance\' and \'the firm\'s cash ratio\') increases or decreases simultaneously. Because of this, we\'d like to invest in companies with high cash ratios.')
    col1,col2 = st.columns([4,5])
    col1.subheader('Bar Plot Comparison by Industry')
    roption=col1.selectbox('Select the industry you would like to evaluate',
                           ('Airlines', 'Telecommunications Equipment', 'Casinos & Gaming', 'Financial Exchanges & Data ', 'Gold', 'Oil & Gas Drilling'))

    col2.plotly_chart(px.bar(combined[combined['gics_sub_industry'] == roption]), x='ticker_symbol', y='cash_ratio', color='ticker_symbol')
    col1.markdown('As depicted from the graph above, the airline firms \'ALK\' and \'AAL\' would be our top 2 stock investments with the highest cash ratios out of the 5 airline stocks in our merged dataset, with cash ratios of 74 and 51 respectively.')
    
    
    st.subheader('Factor 2: Current Ratio')
    st.markdown('According to Investopedia, \"The current ratio is a liquidity ratio that measures a company\’s ability to pay short-term obligations or those due within one year. It tells investors and analysts how a company can maximize the current assets on its balance sheet to satisfy its current debt and other payables. A current ratio that is in line with the industry average or slightly higher is generally considered acceptable. A current ratio that is lower than the industry average may indicate a higher risk of distress or default. Similarly, if a company has a very high current ratio compared with its peer group, it indicates that management may not be using its assets efficiently.\"')
    
    airlines_2015 = airlines_2015.copy()
    current_assets = airlines_2015['total_current_assets']
    current_liabilities = airlines_2015['total_current_liabilities']
    airlines_2015['current_ratio'] = current_assets / current_liabilities
    airlines_2015['c_r_industry_average'] = airlines_2015['current_ratio'].mean()  
    current_ratio_bar = px.bar(airlines_2015, x='ticker_symbol', y='current_ratio', title='Current Ratio', 
                           hover_data=['total_current_assets', 'total_current_liabilities'], 
                           color='ticker_symbol', text_auto=True, 
                           labels={'current_ratio':'Current Ratio', 'ticker_symbol':'Ticker Symbol'},
                           
                            )
    current_ratio_bar.update_layout(title_font_size=25, title_x=0.5, xaxis = dict(
    tickfont = dict(size=15)))
    current_ratio_bar.update_traces(textfont_size=15, textposition='inside', textfont_color='black',
                                texttemplate='<b>%{y:.2f}</b>', 
                                hovertemplate='''Ticker Symbol: %{x} <br>Current Ratio: %{y:.4f}
                                <br>Total Current Assets: %{customdata[0]:$,}<br>Total Current Liabilities: %{customdata[1]:$,}'''
                               )

    # Setting the benchmark of the bar plot as the industry average as calculated above
    dfs = pd.DataFrame({'bins': ['AAL', 'ALK', 'DAL', 'LUV', 'UAL'], 'returns': [0.7339214, 0.9208195, 0.516718, 0.5433432, 0.6305784]})
    dfs['benchmark'] = [0.669076, 0.669076, 0.669076, 0.669076, 0.669076]
    current_ratio_bar.add_traces(go.Scatter(x=dfs.bins, y=dfs.benchmark, mode = 'lines', 
                                        name='Industry Average',
                                       line_color='black', line_width=4
                                    ))
    current_ratio_bar.update_yaxes(range=(0,1), showgrid=False)
    current_ratio_bar.update_xaxes(showgrid=False)
    
    st.plotly_chart(current_ratio_bar)
    st.markdown('As shown from the \'Current Ratio\' bar graph above, all airline firms in the U.S stock market pertains a current ratio below 1, indicating the lack of liquid assets to pay off short-term(within 1 year in this case) debts for all firms in the airline industry. Specifically, companies AAL and UAL are slightly higher/lower(within 0.1) than the average current ratio for firms in the airline industry: 0.66907, which is considered an acceptable performance relative to its competitor. While the firms DAL and LUV are lower than the average current ratio for firms in the airline industry, with a current ratio of 0.516718 and 0.5433432 respectively, indicating that at the current stage, the firm is unable to pay off nearly half of its short term debts. On the other hand, Alaska Air Group, Inc.(ALK) are higher than the average current ratio for firms in the airline industry, suggesting the company\'s high capability of paying off short term obligations relative to the performance of firms in the airline industry; On the other hand, the high current ratio of ALK relative to the average current ratio of the airline industry may indicate the underutilization of resources by the firm\'s management team. ')
    st.markdown('As a recap, our purpose in calculating the current ratio is to determine for the investors the top airline stocks to invest in the U.S stock market which is the least likely to experience bankrupcy relative to its peer group. In this case, although Alaska Air Group, Inc. (ALK) may be using its resources inefficiently, it is still ranked 1st in terms of current ratio out of its competitors, which in other words, in the short term the firm is least likely to experience bankrupcy due to its relatively high asset and debt ratio in the airline industry.')
    
    st.header('Return on Investment')
    st.subheader('Factor 1: Volatility(Standard Deviation) of Stock Prices')
    st.markdown('The standard deviation of stock prices is a vital piece of information regarding its volatility and the extent of investment risk for stock investors. Specifically, standard deviations measures the dispersion of a dataset(the closing prices of stocks in this case) around the mean. Furthermore, the standard deviation is derived through square rooting the variance, which is calculated by summing the squared difference between each data point and the mean of the dataset, then divided by the number of datapoints subtracted by one. Since we\'re squaring the difference between each data point and the mean, the standard deviation for each stock can be deduced of being "double-sided": on one side the standard deviation could represent the stock\'s potential to rise in terms of price, while on the other hand, this measurement of volatility could indicate the stock\'s potential to drop in its prices. Therefore in order to guarentee a positive return rate of the investment in airline stocks, we must select a firm that is the lowest in the standard deviation of its stock prices as relative to its competitors.')
    st.markdown('To make the data presentation easier to comprehend, we will first visualize the trends/changes of each airline stock\'s daily closing prices during the 2010-2015 time period.')
    
    all_prices = all_prices.copy()
    all_prices['AAL_close'] = all_prices.loc[all_prices['symbol'] == 'AAL', 'close']
    all_prices['ALK_close'] = all_prices.loc[all_prices['symbol'] == 'ALK', 'close']
    all_prices['DAL_close'] = all_prices.loc[all_prices['symbol'] == 'DAL', 'close']
    all_prices['LUV_close'] = all_prices.loc[all_prices['symbol'] == 'LUV', 'close']
    all_prices['UAL_close'] = all_prices.loc[all_prices['symbol'] == 'UAL', 'close']
    volatility_line = px.line(all_prices, x='date', y=[all_prices['AAL_close'], all_prices['ALK_close'],
                          all_prices['DAL_close'], all_prices['LUV_close'], 
                          all_prices['UAL_close']], title='Airline Stock Closing Prices', 
                          labels={'date': 'Date', 'value':'Value ($USD)', 'variable':'Variable'}
                         )
    volatility_line.update_layout(title_font_size=25, title_x=0.5, legend_font_size=14)
    # Removing the '_close' part from every legend variable to make the data more 
    # presentable
    newnames = {'AAL_close':'AAL', 'ALK_close':'ALK', 'DAL_close':'DAL', 'LUV_close':'LUV', 'UAL_close':'UAL'}
    volatility_line.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )
   volatility_line.update_xaxes(showgrid=True, gridwidth=1, gridcolor='Black')
   volatility_line.update_yaxes(showgrid=True, gridwidth=1, gridcolor='Black')
   st.plotly_chart(volatility_line)
   st.markdown('As shown on the line graph above, in terms of volatility, we would definitely not invest in the airline firm ALK due to its various large drops as in the year 2012 and 2014; Also, the company ALK pertains a high frequency of approximate 10 dollar drops regarding its closing prices over the time span of 2010-2016 as compared to its competitors, which demonstrates the stock\'s liability to change rapidly and unpredictably, as well as the high risk the investment accompanies. On the other hand, the other four airline stocks seems to be showing a relatively stable upwards trend, with only one to two approximate 10 dollar drops during the year 2015.') 
    
   # In order to calculate the volatility of stock prices:
   # 1. Find the mean of the closing prices and assigning the corresponding values to 
   # a new column
   airline = {'AAL':all_prices.loc[all_prices['symbol'] == 'AAL', 'close'],'ALK':all_prices.loc[all_prices['symbol'] == 'ALK', 'close'], 'DAL':all_prices.loc[all_prices['symbol'] == 'DAL', 'close'], 'LUV':all_prices.loc[all_prices['symbol'] == 'LUV', 'close'], 'UAL':all_prices.loc[all_prices['symbol'] == 'UAL', 'close']}
   airline = airline.copy()
   airline_standard_deviation = []
   for key in airline:
       airline_mean = airline[key].mean()
       # 2. Calculate the variance for the closing prices of each airline stock
       difference = airline[key] - airline_mean
       difference_squared = difference ** 2
       squared_sum = difference_squared.sum()
       variance = squared_sum / (len(difference) - 1)
       airline_standard_deviation = variance   
       # 3. Finally, calculate the standard deviation for the stock prices of each airline firm         
       airline[key] = airline_standard_deviation ** (1/2)
       
   airline_s_d = pd.DataFrame(index=[0,1,2,3,4], data={'ticker_symbol':['AAL', 'ALK', 'DAL', 'LUV', 'UAL'], 'standard_deviation':[15.437005025313345,16.078078199384183,14.594517078380926,12.168414554616513,15.537090072082089]})
   airline_standard_deviation = px.bar(airline_s_d, x='ticker_symbol', y='standard_deviation', title='Standard Deviation', text_auto=True, labels={'standard_deviation':'Standard Deviation', 'ticker_symbol':'Ticker Symbol'}, color='ticker_symbol')
   airline_standard_deviation.update_layout(title_font_size=25, title_x=0.5)
   airline_standard_deviation.update_xaxes(tickfont=dict(size=15), showgrid=False)
   airline_standard_deviation.update_yaxes(tickfont=dict(size=12), range=(0,20), showgrid=False)
   airline_standard_deviation.update_traces(textfont_size=15, textposition='outside',
                                         texttemplate='<b>%{y}</b>'
                                        )
   st.plotly_graph(airline_standard_deviation)
   st.markdown('Unsurprisingly, as corresponding to our line graph visualization of the volatility of the closing prices of airline stocks above, the firm ALK with a standard deviation of 16.07808 ranks 1st as compared to its peer group; While the closing prices of the firms AAL, DAL, and UAL pertains similar standard deviations of around 15. Moreover, while the standard deviations of AAL, ALK, DAL, and UAL are relatively similar, there is still a gap between the standard deviation of LUV, indicating the firm\'s relative low risk of investment. Therefore in terms of volatility of the airline stocks, the firm LUV would definitely be our top stock to invest.')
   
   st.subheader('Factor 3: Relative Price Strength')
   st.markdown('Relative price strength measures the ratio between a stock\'s and market\'s price trend, and are widely utilized in technical analysis for the return rate of a stock. On the other hand, relative price strength (RPS) could also be misleading because the calculation process (dividing the price trend of the market by that of the stock) doesn\'t take into account risk factors(e.g longevity risk). Moreover, an RPS(relative price strength) greater than 1 indicates that the stock outperformed the market, and an RPS lower than 1 suggests that the stock underperformed the market, while an RPS equivalent to 1 indicates that the stock performed on par with the market.')
   
   # Formula: Relative Price Strength = Trend Price of a Stock / Trend Price of the Market
   # Trend Price of a Stock = the percentage of stock price changed over a period of time
   # Trend Price of the Market = the percentage of market change over a period of time
   # Since we are comparing the 5 stocks in the airline industry, in this case we could
   # simply switch the denominator of the RPS formula to the trend price of the airline
   # industry
   initial_trend_price_airline = (all_prices.iloc[0,3] + all_prices.iloc[1208,3] + all_prices.iloc[2416,3]
                       + all_prices.iloc[3624,3] + all_prices.iloc[4832,3]) / 5
   end_trend_price_airline = (all_prices.iloc[1207,3] + all_prices.iloc[2415,3] + all_prices.iloc[3625,3]
                       + all_prices.iloc[4831,3] + all_prices.iloc[6039,3]) / 5
   trend_price_airline = (end_trend_price_airline - initial_trend_price_airline) / initial_trend_price_airline

   AAL_trend_price = (all_prices.iloc[1207,3] - all_prices.iloc[0,3]) / all_prices.iloc[0,3]
   ALK_trend_price = (all_prices.iloc[2415,3] - all_prices.iloc[1208,3]) / all_prices.iloc[1208,3]
   DAL_trend_price = (all_prices.iloc[3625,3] - all_prices.iloc[2416,3]) / all_prices.iloc[2416,3]
   LUV_trend_price = (all_prices.iloc[4831,3] - all_prices.iloc[3624,3]) / all_prices.iloc[3624,3]
   UAL_trend_price = (all_prices.iloc[6039,3] - all_prices.iloc[4832,3]) / all_prices.iloc[4832,3]
   # Substituting the variables into the formula: Trend Price of a Stock / Trend Price of 
   # the Airline Industry
   AAL_RPS = AAL_trend_price / trend_price_airline
   ALK_RPS = ALK_trend_price / trend_price_airline
   DAL_RPS = DAL_trend_price / trend_price_airline
   LUV_RPS = LUV_trend_price / trend_price_airline
   UAL_RPS = UAL_trend_price / trend_price_airline
   # Combining the five RPS values as listed above and combining them into a single pandas
   # dataframe for us to plot the bar chart afterwards easier.
   RPS_df = pd.DataFrame(index=[0,1,2,3,4], data={'ticker_symbol':['AAL', 'ALK', 'DAL', 'LUV', 'UAL'], 'RPS':[AAL_RPS, ALK_RPS, DAL_RPS, LUV_RPS, UAL_RPS]})
   # Plotting a bar graph for the RPS values of each airline stock
   airlines_rps = px.bar(RPS_df, x='ticker_symbol', y='RPS', color='ticker_symbol', text_auto=True, labels={'ticker_symbol':'Ticker Symbol'}, title='Relative Price Strength (RPS)')
   airlines_rps.update_layout(title_font_size=25, title_x=0.5)
   airlines_rps.update_traces(textfont_size=15, textposition='outside')
   airlines_rps.update_xaxes(tickfont=dict(size=15), showgrid=False)
   airlines_rps.update_yaxes(tickfont=dict(size=12), range=(-5,25), showgrid=False)
   dfs = pd.DataFrame({'bins': ['AAL', 'ALK', 'DAL', 'LUV', 'UAL'], 'returns': [21.10048, 2.102004, -2.657386, 0.2936191, 8.53573]})
   dfs['benchmark'] = [1, 1, 1, 1, 1]
   airlines_rps.add_traces(go.Scatter(x= dfs.bins, y=dfs.benchmark, mode = 'lines', name='Benchmark', line_color='black'))
   
   st.plotly_graph(airlines_rps)
   st.markdown('In the bar graph above, the airline firm AAL and UAL greatly outperformed the market: with an RPS of 21.10048 and 8.53573 respectively, while followed by ALK with an RPS of 2.102004. On the other hand, companies DAL and LUV underperformed the market with an RPS of -2.657386 and 0.2936191 respectively. In terms of the relative price strength of stocks, we desire the values to be as high as possible, since the greater the RPS value, the greater the margin which the firm outperformed the market, hence suggesting a relatively high return rate on investment. Therefore in this case our desired investment would be on the stock AAL.')
    
   
    
   
    
if selected == 'Conclusion':
    st.title('Conclusion')
	def load_lottieurl(url: str):
		r = requests.get(url)
		if r.status_code != 200:
			return None
		return r.json()
	lottie_coding = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_qp1q7mct.json")
	st_lottie(
		lottie_coding,
		speed=1,
		reverse=False,
		loop=True,
		quality="low", # medium ; high
		height=None,
		width=600,
		key=None,
		)
	
st.markdown('In terms of financial performance, American Airline Group Inc.(with ticker symbol AAL) ranks top in both our cash ratio and current ratio analysis by a decent margin, with 74 and 0.92 respectively, indicating the firm\'s relatively outstanding ability in terms of liquidity in the airline industry, which could be potentially an indicator for sustained high performances in the stock market. While in terms of return on investment, ALK would also be our top investment option due to its relatively stable performance in the stock market and low investment risk, with a standard deviation of its stock prices of 0.92 and a relative price strength of 2.102004(outperforming the market by 1.102004).')
st.markdown('Therefore, American Airline Group Inc. would be our top airline stock to invest in the S&P 500 index in the year 2016.')
    
    
if selected == 'Bibliography':
    st.title('Bibliography')
    st.header('Original Datasets')
    st.markdown('Gawlik, D. (2017, February 22). New York Stock Exchange. Kaggle. Retrieved September 17, 2022, from https://www.kaggle.com/datasets/dgawlik/nyse ')
    st.header('Other Resources')
    st.markdown('Fernando, J. (2022, August 23). Current ratio explained with formula and examples. Investopedia. Retrieved August 23, 2022, from https://www.investopedia.com/terms/c/currentratio.asp')
    st.markdown('Hayes, A. (2022, September 13). Volatility: Meaning in finance and how it works with stocks. Investopedia. Retrieved August 19, 2022, from https://www.investopedia.com/terms/v/volatility.asp')
    st.markdown('Hayes, A. (2022, June 22). A breakdown on how the Stock Market Works. Investopedia. Retrieved September 14, 2022, from https://www.investopedia.com/articles/investing/082614/how-stock-market-works.asp ')



