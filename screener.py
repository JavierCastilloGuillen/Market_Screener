"""
This screener the skeleton for a basic market screener. It will help you with:

1. Market Technical Screening
2. Market Alerts Signals
3. Further Analysis you might require

Main difference is on this script you will NOT BE STORING data on your local machine. With it
pros and cons. Because it doesn't store data is computationally more efficient and fast. 

For the example, the output of the screener is a prompt print with 
the list of tickers stored on the list variables. You can use this lists for further analyisis or
add more.

Example on the script:

country ='Argentina' <- Change this country for the required one
days_back = 120 <- Data gathering from this day. Will impact on the indicators (200SMA won't work on 120 days of data ;-) )
stocks = investpy.get_stocks_overview(country, n_results=1000) <- n_results=1000 For wider markets go for bigger results.


"""

import investpy
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# List to store variables after screener is launched

b_out = []
cons = []
mcd_up = []
mcd_up0 = []
mcd_d = []
mcd_d0 = []
bb_up  = []
already_bb_up = []
bb_d  = []
already_bb_d = []
rsi_d = []
on_rsi_d = []
on_rsi_up = []
rsi_up = []
rsi_bf_d = []
rsi_bf_up = []

# Functions area. Create here as many functions as required for the screener. 
# Some basic technical examples shown (MACD, RSI, BB) and some price actions Consolidation and Breakout.


def MACD_signal_up(df):
	"""
	This Function will analyze the SIGNAL UP on the MACD of the asset
	Asset MACD on Crossover SIGNAL and Asset MACD Crossover below 0

	"""	
	from ta.trend import MACD
	indicator_macd = MACD(df['Adj Close'])
	df['MACD'] = indicator_macd.macd()
	df['Signal']= indicator_macd.macd_signal()
	df['MACD Histogram']= indicator_macd.macd_diff()
	df['Below_0_Crossover_MACD_Signal'] = False
	df['Simple_Crossover_MACD_Signal'] = False

	# MACD Crossover logics
	if (df[-2:]['MACD'].values[0] <= df[-1:]['MACD'].values[0]) and (df[-2:]['MACD'].values[0] <= df[-2:]['Signal'].values[0]) and (df[-1:]['MACD'].values[0]>=df[-1:]['Signal'].values[0]):
		

		# MACD crossover AND Below 0	
		if (df[-2:]['MACD'].values[0] <= df[-1:]['MACD'].values[0]) and (df[-2:]['MACD'].values[0] <= df[-2:]['Signal'].values[0]) and (df[-1:]['MACD'].values[0]>=df[-1:]['Signal'].values[0]) and df[-1:]['MACD'].values[0]<= 0:
			mcd_up0.append(symbol)
			df['Below_0_Crossover_MACD_Signal'][-1] = True
		else:
			mcd_up.append(symbol)
			df['Simple_Crossover_MACD_Signal'][-1] = True
			df['Below_0_Crossover_MACD_Signal'][-1] = False
			return True
	return False

def MACD_signal_down(df):
	"""
	This Function will analyze the SIGNAL DOWN on the MACD asset
	Asset MACD on Crossunder SIGNAL and Asset MACD Crossunder above 0

	"""	
	from ta.trend import MACD
	indicator_macd = MACD(df['Adj Close'])
	df['MACD'] = indicator_macd.macd()
	df['Signal']= indicator_macd.macd_signal()
	df['MACD Histogram']= indicator_macd.macd_diff()
	df['Simple_Crossdown_MACD_Signal'] = False
	df['Above_0_Crossunder_MACD_Signal'] = False

	#	MACD croosunder
	if (df[-2:]['MACD'].values[0] >= df[-1:]['MACD'].values[0]) and (df[-2:]['MACD'].values[0] >= df[-2:]['Signal'].values[0]) and (df[-1:]['MACD'].values[0]<=df[-1:]['Signal'].values[0]):
		# MACD crossunder AND above 0	
		if (df[-2:]['MACD'].values[0] >= df[-1:]['MACD'].values[0]) and (df[-2:]['MACD'].values[0] >= df[-2:]['Signal'].values[0]) and (df[-1:]['MACD'].values[0]<=df[-1:]['Signal'].values[0]) and df[-1:]['MACD'].values[0]>= 0:
			mcd_d0.append(symbol)
			df['Above_0_Crossunder_MACD_Signal'][-1] = True
			
		else:
			mcd_d.append(symbol)
			df['Simple_Crossdown_MACD_Signal'][-1] = True
			df['Above_0_Crossunder_MACD_Signal'][-1] = False
			return True
		return False

def Bollinger_signal_up(df, window=20, window_dev=2):
	"""
	This Function will analyze the Bollinger UP on the asset
	Bollinger Up signal, Asset already above upper Bollinger Band

	"""	

	from ta.volatility import BollingerBands
	indicator_bb = BollingerBands(df["Adj Close"], 20, 2)
	df['bb_bbm'] = indicator_bb.bollinger_mavg()
	df['bb_bbh'] = indicator_bb.bollinger_hband()
	df['bb_bbl'] = indicator_bb.bollinger_lband()
	df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()
	df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()
	df['Boll_UP'] = False
	df['Boll_UP2']= False

	# Asset on Upper Bollinger Band Signal
	if (df[-2:]['bb_bbhi'].values[0] == 0) and (df[-1:]['bb_bbhi'].values[0] == 1):
		df['Boll_UP'][-1] = True
		bb_up.append(symbol)
		return True
	
	# Asset already avobe Upper Bollinger Band
	elif (df[-2:]['bb_bbhi'].values[0] == 1) and (df[-1:]['bb_bbhi'].values[0] == 1):
		df['Boll_UP2'][-1] = True
		already_bb_up.append(symbol)
		return True
	return False

def Bollinger_signal_down(df, window=20, window_dev=2):
	"""
	This Function will analyze the Bollinger DOWN on the asset
	Bollinger down signal, Asset already below lower Bollinger Band

	"""	

	from ta.volatility import BollingerBands
	indicator_bb = BollingerBands(df["Adj Close"], 20, 2)
	df['bb_bbm'] = indicator_bb.bollinger_mavg()
	df['bb_bbh'] = indicator_bb.bollinger_hband()
	df['bb_bbl'] = indicator_bb.bollinger_lband()
	df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()
	df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()
	df['Boll_Down'] = False
	df['Boll_Down2']= False

	# Asset on Signal Lower Bollinger Band
	if (df[-2:]['bb_bbli'].values[0] == 0) and (df[-1:]['bb_bbli'].values[0] == 1):	
		bb_d.append(symbol)
		df['Boll_Down'][-1]= True
		return True
	
	# Asset already below lower Bollinger
	elif (df[-2:]['bb_bbli'].values[0] == 1) and (df[-1:]['bb_bbli'].values[0] == 1):
		already_bb_d.append(symbol)	
		df['Boll_Down2'][-1]= True
		return True
	return False

def RSI_signal_up(df, window = 14):
	"""
	This Function will analyze the SIGNAL UP on the RSI asset
	Overbought signal, Asset already Overbought and asset back to range from Overbought

	"""	

	from ta.momentum import RSIIndicator
	indicator_rsi= RSIIndicator(df['Adj Close'], window= 14)
	df['RSI'] = indicator_rsi.rsi()
	df['RSI_Overbought'] = False
	
	# Asset back to range 70-30 from Overbought
	if (df[-2:]['RSI'].values[0] >= 70) and (df[-1:]['RSI'].values[0] <= 70):
		rsi_bf_up.append(symbol)

	# Asset on RSI > 70		
	if (df[-1:]['RSI'].values[0] >= 70):
		on_rsi_up.append(symbol)
		df['RSI_Overbought'][-1] = True
		
		# RSI Overbought SIGNAL	
		if (df[-2:]['RSI'].values[0] <= 70) and (df[-1:]['RSI'].values[0] >= 70):
			rsi_up.append(symbol)
			return True
	return False

def RSI_signal_down(df, window= 14):
	"""
	This Function will analyze the SIGNAL DOWN on the RSI asset
	Oversold signal, Asset already oversold and asset back to range from oversold

	"""	

	from ta.momentum import RSIIndicator
	indicator_rsi= RSIIndicator(df['Adj Close'], window= 14)
	df['RSI'] = indicator_rsi.rsi()
	df['RSI_Oversold'] = False
	
	# Asset back to range 30-70 from Oversold
	if (df[-2:]['RSI'].values[0] <= 30) and (df[-1:]['RSI'].values[0] >= 30):
		rsi_bf_d.append(symbol)

	# Asset on RSI < 30
	if (df[-1:]['RSI'].values[0] <= 30):
		on_rsi_d.append(symbol)
		df['RSI_Oversold'][-1] = True
		
		# RSI just crossed down SIGNAL
		if (df[-2:]['RSI'].values[0] >= 30) and (df[-1:]['RSI'].values[0] <= 30):
			rsi_d.append(symbol)
			return True
	return False

def consolidating_signal(df, perc = 3.5):
	"""
	This Function will analyze the asset is consolidating within the perc range.
	Ex: perc =3.5 means the closing price within the last 15 sessions, hasn't changed 
	further than 3.5%

	"""	
	range_of_candlesticks= df[-15:]
	max_close_price = range_of_candlesticks['Adj Close'].max()
	min_close_price = range_of_candlesticks['Adj Close'].min()
	threshold_detection = 1 - (perc / 100)
	if min_close_price > (max_close_price * threshold_detection):
		cons.append(symbol)
		return True
	return False

def breaking_out_signal(df, perc=1,):
	"""
	This Function will analyze the an asset which is coming out from a consolidation
	period.
	
	[perc] = will be the threshold in % for the closing price to determinate if the asset is 
	under consolidation.

	On the example perc = 1, the asset will be closing within 1% range on the last 15 sessions and then
	on current candle is breaking out.

	"""	
	last_close = df[-1:]['Adj Close'].values[0]
	if consolidating_signal(df[:-1], perc = perc):
		recent_close = df[-16:-1]
		if last_close > recent_close['Adj Close'].max():
			b_out.append(symbol)
			return True
	return False


# Screener parameters (country, days_back and n_results) depending on indicators and market must be changed.

country ='Argentina'
days_back = 120
today = datetime.now()
start = today -timedelta(days_back)
today = datetime.strftime(today, '%d/%m/%Y')
start = datetime.strftime(start, '%d/%m/%Y')
stocks = investpy.get_stocks_overview(country, n_results=1000)
stocks = stocks.drop_duplicates(subset='symbol')

# Dates
today = datetime.now()
start = today -timedelta(days_back)
today = datetime.strftime(today, '%d/%m/%Y')
start = datetime.strftime(start, '%d/%m/%Y')

# Screener launch count variable added to while loop limit if necessary to control the API-HTTP call/requests.
# Uncomment while and indent for if necessary.

count = 0
# while count < (n) :
for symbol in stocks['symbol']:
    try:
        # count += 1       
        df = investpy.get_stock_historical_data(stock=symbol,country=country,from_date=f'{start}', to_date=f'{today}')
        time.sleep(0.25)
        df= df.rename(columns={"Close": "Adj Close"})
        if breaking_out_signal(df, 3):
            pass		
        if consolidating_signal(df, perc=2):
            pass
        if RSI_signal_up(df):
            pass
        if RSI_signal_down(df):
            pass
        if MACD_signal_up(df):
            pass
        if MACD_signal_down(df):
            pass
        if Bollinger_signal_up(df):
            pass
        if Bollinger_signal_down(df):
            pass
        
    except Exception as e:
        print(f'No data on {symbol}')
        print(e)


# OUTPUT => For the example just a print, but you've got the tickers stored on the variables to do further analysis


print(f'--------- GENERAL MARKET SCREENER in {country} for {len(stocks)} assets: data analyzed from {start} until {today} --------\n')
print('--- BOLLINGER ANALYSIS --- \n')
print(f'The stocks on SIGNAL BOLLINGER UP are:\n==> {bb_up}\n')
print(f'The stocks are already in BOLLINGER UP:\n==> {already_bb_up}\n')
print(f'The stocks on SIGNAL BOLLINGER DOWN are:\n==> {bb_d}\n')
print(f'The stocks are already in BOLLINGER_DOWN:\n==> {already_bb_d}\n')
print('--- MACD ANALYSIS --- \n')
print(f'The stocks on MACD SIGNAL UP are:\n==> {mcd_up}\n')
print(f'The stocks on MACD SIGNAL UP BELOW 0 are:\n==> {mcd_up0}\n')
print(f'The stocks on MACD SIGNAL DOWN are:\n==> {mcd_d} \n')
print(f'The stocks on MACD SIGNAL DOWN above 0 are:\n==> {mcd_d0}\n')
print('--- RSI ANALYSIS --- \n')
print(f'The stocks on OVERBOUGHT SIGNAL [RSI] are:\n==> {rsi_up}\n')
print(f'The stocks on OVERSOLD SIGNAL [RSI] are:\n==> {rsi_d}\n')
print(f'The stocks went to RANGE from OVERSOLD are:\n==> {rsi_bf_d}\n')
print(f'The stocks went to RANGE from OVERBOUGHT are:\n==> {rsi_bf_up}\n')
print(f'The stocks on OVERBOUGHT [RSI] are:\n==> {on_rsi_up}\n')
print(f'The stocks on OVERSOLD [RSI] are:\n==> {on_rsi_d}\n')
print('--- PRICE ACTION ANALYSIS --- \n')
print(f'The stocks on CONSOLIDATION are:\n==> {cons}\n')
print(f'The stocks on BREAKOUT are:\n==> {b_out}\n')



