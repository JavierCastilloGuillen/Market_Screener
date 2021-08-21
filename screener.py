
import pandas as pd
import datetime as dt
import pandas_datareader as pdr
import os
import investpy
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


# 1. Creamos la carpeta donde se almacenan temporalmente los .csv
# 1. We will create the path were our temporary data will be stored in .csv
if not os.path.exists('data'):
    os.mkdir('data')

# 2. Para este ejemplo, leeremos los activos del documento especies.csv.
# 2. On this particular script, we will read our data from especies.csv. 
stocks = pd.read_csv('especies.csv')

# 3. Seleccionamos la ruta en la que estará nuestro proyecto con el final en \data puesto que ahí se almacenará la información.
# 3. Select the path in where our project will be stored. Remember end on \data puesto que ahí se almacenará la información.
path = (r"C:\Users\javie\Desktop\Screener_Arg\data")

# 4. Manejo de fechas. Recordad modificar days_back si necesitamos indicadores con más longitud de datos (mm200, etc.)
# 4. Date handling. Remember to modify days_back in case we need indicators with longer data (sma200, etc.)

days_back = 50


today = datetime.now()
start = today -timedelta(days_back)
today = datetime.strftime(today, '%d/%m/%Y')
start = datetime.strftime(start, '%d/%m/%Y')



# 5. Proceso de solicitud de datos a través de la librería investpy para el documento especies.csv columna (Ticker)
# 5. Data gathering process through investpy library for especies.csv on (Ticker) column

count = 0
for ticker in stocks['Ticker']:
	try:
		count+= 1
		time.sleep(0.5)
		df = investpy.get_stock_historical_data(stock=ticker,country='Argentina',from_date=f'{start}', to_date=f'{today}')
		# ----> if we wish see the data ;) print(df)
		df= df.rename(columns={"Close": "Adj Close"})
		print(f'Analyzing {count}.....{ticker}')
		print(df.tail())
		df.to_csv(fr'data/{ticker}.csv')
		time.sleep(1)
	except Exception as e:
		print(e)
		print(f'No data on {ticker}')


# 6. A continuación definiremos algún ejemplo de funciones técnicas utilizando 
# la librería TA para análisis técnico. Modificar al gusto de cada usuario.
# 6. Following we will write some functions in order to retreive the technical 
# indicator from TA, add it to our dataframe and define logics for the signals.

def MACD_signal_up(df):
#    Load the indicator:
	from ta.trend import MACD
	indicator_macd = MACD(df['Adj Close'])
	df['MACD'] = indicator_macd.macd()
	df['Signal']= indicator_macd.macd_signal()
	df['MACD Histogram']= indicator_macd.macd_diff()
	df['Below_0_Crossover_MACD_Signal'] = False
	df['Simple_Crossover_MACD_Signal'] = False

#    Define the logics:
	if (df[-2:]['MACD'].values[0] <= df[-1:]['MACD'].values[0]) and (df[-2:]['MACD'].values[0] <= df[-2:]['Signal'].values[0]) and (df[-1:]['MACD'].values[0]>=df[-1:]['Signal'].values[0]):
		

		# MACD crossover AND Below 0	
		if (df[-2:]['MACD'].values[0] <= df[-1:]['MACD'].values[0]) and (df[-2:]['MACD'].values[0] <= df[-2:]['Signal'].values[0]) and (df[-1:]['MACD'].values[0]>=df[-1:]['Signal'].values[0]) and df[-1:]['MACD'].values[0]<= 0:
			print(f'{symbol} MACD UP alert below 0')
			df['Below_0_Crossover_MACD_Signal'][-1] = True

		else:
			print(f'{symbol} MACD UP alert')
			df['Simple_Crossover_MACD_Signal'][-1] = True
			df['Below_0_Crossover_MACD_Signal'][-1] = False
			return True

	return False

def MACD_signal_down(df):
	from ta.trend import MACD
	indicator_macd = MACD(df['Adj Close'])
	df['MACD'] = indicator_macd.macd()
	df['Signal']= indicator_macd.macd_signal()
	df['MACD Histogram']= indicator_macd.macd_diff()
	df['Simple_Crossdown_MACD_Signal'] = False
	df['Above_0_Crossunder_MACD_Signal'] = False
#	MACD croosunder above
	if (df[-2:]['MACD'].values[0] >= df[-1:]['MACD'].values[0]) and (df[-2:]['MACD'].values[0] >= df[-2:]['Signal'].values[0]) and (df[-1:]['MACD'].values[0]<=df[-1:]['Signal'].values[0]):
		# MACD crossover AND above 0	
		if (df[-2:]['MACD'].values[0] >= df[-1:]['MACD'].values[0]) and (df[-2:]['MACD'].values[0] >= df[-2:]['Signal'].values[0]) and (df[-1:]['MACD'].values[0]<=df[-1:]['Signal'].values[0]) and df[-1:]['MACD'].values[0]>= 0:
			print(f'{symbol} MACD DOWN above 0')
			df['Above_0_Crossunder_MACD_Signal'][-1] = True
			
		else:
			print(f'{symbol} MACD DOWN alert')
			df['Simple_Crossdown_MACD_Signal'][-1] = True
			df['Above_0_Crossunder_MACD_Signal'][-1] = False
			return True
		return False

def Bollinger_signal_up(df, window=20, window_dev=2):
#    Load the indicator
	from ta.volatility import BollingerBands
	indicator_bb = BollingerBands(df["Adj Close"], 20, 2)
	df['bb_bbm'] = indicator_bb.bollinger_mavg()
	df['bb_bbh'] = indicator_bb.bollinger_hband()
	df['bb_bbl'] = indicator_bb.bollinger_lband()
	df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()
	df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()
	df['Boll_UP'] = False
	df['Boll_UP2']= False

#    Logics:
#	Stocks just above of HIGH bollinger
	if (df[-2:]['bb_bbhi'].values[0] == 0) and (df[-1:]['bb_bbhi'].values[0] == 1):
		df['Boll_UP'][-1] = True
		print(f'{symbol} Went above HIGH bollinger JUST NOW')
		return True
	elif (df[-2:]['bb_bbhi'].values[0] == 1) and (df[-1:]['bb_bbhi'].values[0] == 1):
		df['Boll_UP2'][-1] = True
		print(f'{symbol} is ALREADY on HIGH bollinger')
		return True
	return False



def Bollinger_signal_down(df, window=20, window_dev=2):
	from ta.volatility import BollingerBands
	indicator_bb = BollingerBands(df["Adj Close"], 20, 2)
	df['bb_bbm'] = indicator_bb.bollinger_mavg()
	df['bb_bbh'] = indicator_bb.bollinger_hband()
	df['bb_bbl'] = indicator_bb.bollinger_lband()
	df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()
	df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()
	df['Boll_Down'] = False
	df['Boll_Down2']= False


	# Stocks just out of LOW bollinger
	if (df[-2:]['bb_bbli'].values[0] == 0) and (df[-1:]['bb_bbli'].values[0] == 1):	
		print(f'{symbol} is below LOWER bollinger JUST NOW')
		df['Boll_Down'][-1]= True
		return True
	elif (df[-2:]['bb_bbli'].values[0] == 1) and (df[-1:]['bb_bbli'].values[0] == 1):	
		print(f'{symbol} is ALREADY in LOWER bollinger')
		df['Boll_Down2'][-1]= True
		return True
	return False

def RSI_signal_up(df, window = 14):
	from ta.momentum import RSIIndicator
	indicator_rsi= RSIIndicator(df['Adj Close'], window= 14)
	df['RSI'] = indicator_rsi.rsi()
	df['RSI_Overbought'] = False
	if (df[-2:]['RSI'].values[0] >= 70) and (df[-1:]['RSI'].values[0] <= 70):
		print(f'{symbol} RSI ALERT just went to range from overbought')

	# RSI went to overbought		
	if (df[-1:]['RSI'].values[0] >= 70):
		print(f'{symbol} is overbought')
		df['RSI_Overbought'][-1] = True
		
		# RSI just crossed overbought	
		if (df[-2:]['RSI'].values[0] <= 70) and (df[-1:]['RSI'].values[0] >= 70):
			print(f'{symbol} RSI ALERT just crossed over')
			return True
	return False

def RSI_signal_down(df, window =14):
	from ta.momentum import RSIIndicator
	indicator_rsi= RSIIndicator(df['Adj Close'], window= 14)
	df['RSI'] = indicator_rsi.rsi()
	df['RSI_Oversold'] = False
	
	if (df[-2:]['RSI'].values[0] <= 30) and (df[-1:]['RSI'].values[0] >= 30):
			print(f'{symbol} RSI ALERT just went to range from oversold')
		# RSI is oversold
	
	if (df[-1:]['RSI'].values[0] <= 30):
		
		print(f'{symbol} is oversold')
		df['RSI_Oversold'][-1] = True
		
		# RSI just crossed down
		if (df[-2:]['RSI'].values[0] >= 30) and (df[-1:]['RSI'].values[0] <= 30):
			print(f'{symbol} RSI ALERT just crossed under')
			return True
	return False


# Price action Functions (candlesticks patterns, consolidations, breakouts etc.)

def consolidating_signal(df, perc = 3.5):

	range_of_candlesticks= df[-15:]
	max_close_price = range_of_candlesticks['Adj Close'].max()
	min_close_price = range_of_candlesticks['Adj Close'].min()
	threshold_detection = 1 - (perc / 100)
	if min_close_price > (max_close_price * threshold_detection):
		return True
	return False

def breaking_out_signal(df, perc=1,):
	last_close = df[-1:]['Adj Close'].values[0]
	if consolidating_signal(df[:-1], perc = perc):
		recent_close = df[-16:-1]
		if last_close > recent_close['Adj Close'].max():
			return True
	return False



###### START SCREENER ########## with our data stored in .CSV format

print(f'------------ START SCREENER: data from {start} until {today}-----------')
print('--------- BREAKOUTS ------------')
for filename in os.listdir(path):
	df = pd.read_csv(path+f'\{filename}')
	symbol = filename.split(".")[0]
	if breaking_out_signal(df, 3):
		print(f'{symbol} is breaking out')
print('---------- CONSOLIDATION ------------')
for filename in os.listdir(path):
	df = pd.read_csv(path+f'\{filename}')
	symbol = filename.split(".")[0]
	if consolidating_signal(df, perc=2):
		print(f'{symbol} is consolidating')
print('---------- RSI ------------------')
for filename in os.listdir(path):
	df = pd.read_csv(path+f'\{filename}')
	symbol = filename.split(".")[0]

	if RSI_signal_up(df):
		print(f'{symbol} is on RSI alert UP')
	if RSI_signal_down(df):
		print(f'{symbol} is on RSI alert DOWN')
print('----------- MACD -------------')
for filename in os.listdir(path):
	df = pd.read_csv(path+f'\{filename}')
	symbol = filename.split(".")[0]

	if MACD_signal_up(df):
		 print(f'{symbol} is on MACD UP')
	if MACD_signal_down(df):
		 print(f'{symbol} is on MACD DOWN')	
print('---------- BOLLINGER ----------')
for filename in os.listdir(path):
	df = pd.read_csv(path+f'\{filename}')
	symbol = filename.split(".")[0]

	if Bollinger_signal_up(df):
		print(f'{symbol} Bollinger Signal UP')
	if Bollinger_signal_down(df):
		print(f'{symbol} Bollinger Signal DOWN')


