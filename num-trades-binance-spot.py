#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Felipe Soares
"""
import numpy
import talib
import requests
import json
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

#=========
criptomoeda = input('DataCrypto Analytics | Criar gráfico de preços e número de negociações |'
                    '\n\n | Twitter @DataCryptoML |'
                    '\n | Github @datacryptoanalytics |'
                    '\n \nDigite o par de criptomoedas listada na Binance: ')

print('\nO par de criptomoeda informada foi: %s'
      '\n\nDataCrypto Analytics esta buscando os valores,'
      ' por favor aguarde alguns segundos!' %(criptomoeda))


root_url = 'https://api.binance.com/api/v1/klines'

symbol = criptomoeda

interval = input('Digite o Timeframe (Exemplo: 15m, 30m, 1h, 1d, 1M): ')

url = root_url + '?symbol=' + symbol + '&interval=' + interval

print(url)


# ===========
def get_bars(symbol, interva = interval ):
   url = root_url + '?symbol=' + symbol + '&interval=' + interval
   data = json.loads(requests.get(url).text)
   df = pd.DataFrame(data)
   df.columns = ['open_time',
                 'o', 'h', 'l', 'c', 'v',
                 'close_time', 'qav', 'num_trades',
                 'taker_base_vol', 'taker_quote_vol', 'ignore']
   df.index = [dt.datetime.fromtimestamp(x/1000.0) for x in df.close_time]
   return df

#============
criptomoeda = get_bars(criptomoeda)

criptomoeda_fechamento = criptomoeda['c'].astype('float')
criptomoeda_abertura = criptomoeda['o'].astype('float')
criptomoeda_num_trades = criptomoeda['num_trades'].astype('float')
criptomoeda_maxima = criptomoeda['h'].astype('float')
criptomoeda_minima = criptomoeda['l'].astype('float')
criptomoeda_volume = criptomoeda['v'].astype('float')
criptomoeda_datas_fechamento = criptomoeda['close_time'].astype('float')
criptomoeda_datas_abertura = criptomoeda['open_time'].astype('float')

#============  Indicadores
cci = talib.CCI(criptomoeda_maxima, criptomoeda_minima, criptomoeda_fechamento, timeperiod=14)
atr = talib.ATR(criptomoeda_maxima, criptomoeda_minima, criptomoeda_fechamento, timeperiod=14)

midpoint = talib.MIDPOINT(criptomoeda_fechamento, timeperiod=14)


real = talib.T3(criptomoeda_fechamento, timeperiod=14)

#rsi = talib.RSI(criptomoeda_fechamento, timeperiod=14)

crows = talib.CDLKICKINGBYLENGTH(criptomoeda_abertura, criptomoeda_maxima, criptomoeda_minima, criptomoeda_fechamento)

def RSI(close,timePeriod):    
    rsi = ta.RSI(criptomoeda_fechamento,timePeriod)
    rsiSell = (rsi>70) & (rsi.shift(1)<=70)
    rsiBuy = (rsi<30) & (rsi.shift(1)>=30)
    return rsiSell,rsiBuy, rsi
# Média movel de 14 dias do Fechamento
criptomoeda_fechamento_mediamovel = criptomoeda_fechamento.rolling(30).mean()
# Média movel de 30 dias do Fechamento
criptomoeda_fechamento_mediamovel100 = criptomoeda_fechamento.rolling(100).mean()
medias = criptomoeda_num_trades.rolling(12).mean()
# Retorno diário percentual
criptomoeda_fechamento_mediamovelDailyReturn = criptomoeda_fechamento.pct_change()
#print('Retorno Diario', criptomoeda_fechamento_mediamovelDailyReturn)
#print('\nMédia Movel 100 Periodos: \n%s' %(criptomoeda_fechamento_mediamovel100 ))
print('Média 100 periodos', criptomoeda_fechamento.mean())
print('Média num_trades', criptomoeda_num_trades.mean())
media = criptomoeda_fechamento.mean()
calc = criptomoeda_num_trades.mean()
#============  Criar Gráfico
#plt.style.use('ggplot')
plt.style.use('bmh')
plt.rcParams['figure.figsize'] = (9,5)
plt.rcParams['font.family'] = 'serif'

#============ Plotar indicadores
plt.subplot(2, 1, 1)
plt.plot(criptomoeda_fechamento, '-', color="black", linewidth=1)
plt.plot(criptomoeda_fechamento_mediamovel, '-', color="red", linewidth=1)
plt.plot(criptomoeda_fechamento_mediamovel100, '-', color="black", linewidth=1)
plt.plot(midpoint, '-', color="orange", linewidth=1)
plt.legend(['Close', 'MA30', 'MA100'], loc=0)
plt.title('DataCrypto Analytics (@DataCryptoML)')
plt.ylabel('Price')

plt.subplot(2, 1, 2)
plt.plot(atr, '-', color="black", linewidth=1)
plt.legend(['RSI', 'MA12'], loc=0)
plt.xlabel('Github: @datacrypto-analytics', fontsize=9)
plt.ylabel('RSI')
plt.gcf().autofmt_xdate()

"""
plt.subplot(2, 1, 2)
plt.plot(criptomoeda_num_trades, '-', color="black", linewidth=1)
plt.plot(medias, '-', color="red", linewidth=1)
plt.legend(['num_trades', 'MA12'], loc=0)
plt.xlabel('Github: @datacrypto-analytics', fontsize=9)
plt.ylabel('Number of Trades')
plt.gcf().autofmt_xdate()
"""
plt.show()
