import pandas as pd
#!pip install nsepy
from nsepy import get_history
from datetime import date
import numpy as np
import matplotlib.transforms as transforms

import matplotlib.pyplot as plt

symbol_index = ['NIFTY SMLCAP 100','NIFTY SMLCAP 250','NIFTY SMLCAP 50','NIFTY MIDCAP 150','NIFTY 50','NIFTY BANK','NIFTY NEXT 50','NIFTY FMCG']
symbol_stock =  ['SBIN', 'RELIANCE', 'HDFCBANK', 'INFY', 'KOTAKBANK','TCS', 'LT', 'HINDUNILVR','ITC']

print("Pre-available Indices:\n\n", symbol_index)
print("\nPre-available Stocks:\n\n", symbol_stock)

inp = int(input("Press: \t 1 for Indices \t 2 for Stocks : "))
sym = ''
if inp == 1:
    sym += input("Enter the symbol name : ")
    if sym not in symbol_index:
        symbol_index.append(symbol)
elif inp == 2:
    sym += input("Enter the symbol name : ")
    if sym not in symbol_stock:
        symbol_stock.append(symbol)
else:
    print("\nInvalid Input")

data1 = []
data1 = pd.DataFrame(data1)
start, end = input("Enter space separated START & END dates in the format %YY,%MM,%DD : ").split()
syear, smonth, sday = map(int, start.split(','))
eyear, emonth, eday = map(int, end.split(','))

df = ''
nf = ''
data1 = []
data1 = pd.DataFrame(data1)
if inp == 1:
    for x in symbol_index:
        data = get_history(symbol=x, start=date(2018,7,1), end=date(2021,12,16), index = True)
        data = pd.DataFrame(data)
        data['Index_Name'] = x
        data1 = pd.concat([data1,data])
        print(x)
        # Save the Data
        data1.to_csv('data.csv', index=True)
        df = pd.read_csv(r'data.csv', index_col = 0, parse_dates = True)
        nf = df[(df['Index_Name']==sym)]
if inp == 2:
    for x in symbol_stock:
        data = get_history(symbol=x, start=date(syear,smonth,sday), end=date(eyear,emonth,eday))
        data = pd.DataFrame(data)
        data1 = pd.concat([data1,data])
        print(x)
        # Save the Data
        data1.to_csv('data.csv', index=True)
        df = pd.read_csv(r'data.csv', index_col = 0, parse_dates = True)
        nf = df[(df['Symbol']==sym)]


def data_resampling(nf, period):
#df = pd.read_clipboard(parse_dates=['Date'], index_col=['Date'])
    logic = {'Open'  : 'first',
             'High'  : 'max',
             'Low'   : 'min',
             'Close' : 'last',
             'Volume': 'sum'}

    dfw = nf.resample(period).apply(logic)
    # set the index to the beginning of the time_period
    dfw.index = dfw.index - pd.tseries.frequencies.to_offset("6D")
    return dfw

def plot(dfw):   
    fig, ax = plt.subplots(figsize=(10,5))
    dfw['Close'].tail().plot(ax = ax)
    ax.set_ylabel("Price")
    if inp == 1:
        ax.set_title(nf['Index_Name'][0]+' '+period[p]+' analysis')
    if inp == 2:
        ax.set_title(nf['Symbol'][0]+' ' +period[p]+' analysis')
    #S3-------------------
    ax.hlines(y=dfw['S3'][-1], xmin=dfw.index[0], xmax=dfw.index[-1], colors='black', linestyles='-', lw=2, label='Buy reversal')
    trans = transforms.blended_transform_factory(
        ax.get_yticklabels()[0].get_transform(), ax.transData)
    ax.text(0,dfw['S3'][-1], "{:.0f}".format(dfw['S3'][-1]), color="black", fontweight= 'bold',transform=trans, 
            ha="right", va="center")
    #R3-------------------
    ax.hlines(y=dfw['R3'][-1], xmin=dfw.index[0], xmax=dfw.index[-1], colors='black', linestyles='-', lw=2, label='Sell reversal zone')
    trans = transforms.blended_transform_factory(
        ax.get_yticklabels()[0].get_transform(), ax.transData)
    ax.text(0,dfw['R3'][-1], "{:.0f}".format(dfw['R3'][-1]), color="black", fontweight= 'bold',transform=trans, 
            ha="right", va="center")
    #S4-------------------
    ax.hlines(y=dfw['S4'][-1], xmin=dfw.index[0], xmax=dfw.index[-1], colors='red', linestyles='-', lw=2, label='Breakdown')
    trans = transforms.blended_transform_factory(
        ax.get_yticklabels()[0].get_transform(), ax.transData)
    ax.text(0,dfw['S4'][-1], "{:.0f}".format(dfw['S4'][-1]), color="red", fontweight= 'bold',transform=trans, 
            ha="right", va="center")
    #S5-------------------
    ax.hlines(y=dfw['S5'][-1], xmin=dfw.index[0], xmax=dfw.index[-1], colors='red', linestyles='--', lw=2, label='Target 1 SHORT')
    trans = transforms.blended_transform_factory(
        ax.get_yticklabels()[0].get_transform(), ax.transData)
    ax.text(0,dfw['S5'][-1], "{:.0f}".format(dfw['S5'][-1]), color="red", fontweight= 'bold',transform=trans, 
            ha="right", va="center")

    #S6-------------------
    ax.hlines(y=dfw['S6'][-1], xmin=dfw.index[0], xmax=dfw.index[-1], colors='red', linestyles=':', lw=2, label='Target 2 SHORT')
    trans = transforms.blended_transform_factory(
        ax.get_yticklabels()[0].get_transform(), ax.transData)
    ax.text(0,dfw['S6'][-1], "{:.0f}".format(dfw['S6'][-1]), color="red", fontweight= 'bold',transform=trans, 
            ha="right", va="center")
    #R4-------------------
    ax.hlines(y=dfw['R4'][-1], xmin=dfw.index[0], xmax=dfw.index[-1], colors='green', linestyles='-', lw=2, label='Breakout')
    trans = transforms.blended_transform_factory(
        ax.get_yticklabels()[0].get_transform(), ax.transData)
    ax.text(0,dfw['R4'][-1], "{:.0f}".format(dfw['R4'][-1]), color="green", fontweight= 'bold',transform=trans, 
            ha="right", va="center")
    #R5-------------------
    ax.hlines(y=dfw['R5'][-1], xmin=dfw.index[0], xmax=dfw.index[-1], colors='green', linestyles='--', lw=2, label='Target 1 LONG')
    trans = transforms.blended_transform_factory(
        ax.get_yticklabels()[0].get_transform(), ax.transData)
    ax.text(0,dfw['R5'][-1], "{:.0f}".format(dfw['R5'][-1]), color="green", fontweight= 'bold',transform=trans, 
            ha="right", va="center")
    #R6-------------------
    ax.hlines(y=dfw['R6'][-1], xmin=dfw.index[0], xmax=dfw.index[-1], colors='green', linestyles=':', lw=2, label='Target 2 LONG')
    trans = transforms.blended_transform_factory(
        ax.get_yticklabels()[0].get_transform(), ax.transData)
    ax.text(0,dfw['R6'][-1], "{:.0f}".format(dfw['R6'][-1]), color="green", fontweight= 'bold',transform=trans, 
            ha="right", va="center")

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.tight_layout(
    plt.show()

def levels(T):    
    pd.options.mode.chained_assignment = None
    T['PP'] = np.nan
    T['S3'] = np.nan
    T['S4'] = np.nan
    T['S5'] = np.nan
    T['S6'] = np.nan
    T['R3'] = np.nan
    T['R4'] = np.nan
    T['R5'] = np.nan
    T['R6'] = np.nan
    T.fillna(0)
    for x in range(len(T)-1):
        O = T['Open'][x]
        C = T['Close'][x]
        L = T['Low'][x]
        H = T['High'][x]
        RANGE = H-L
        T['R3'][x+1] = C + RANGE * 1.1/4
        T['R4'][x+1] = C + RANGE * 1.1/2
        T['R6'][x+1] = (H/L)*C
        T['R5'][x+1] = T['R4'][x+1] + 1.168 * (T['R4'][x+1] - T['R3'][x+1])
        R4 = C + RANGE * 1.1/2

    #     R2 = C + RANGE * 1.1/6
    #     R1 = C + RANGE * 1.1/12
        T['PP'][x+1] = (H+L+C) / 3
    #     S1 = C - RANGE * 1.1/12
    #     S2 = C - RANGE * 1.1/6
        T['S3'][x+1] = C - RANGE * 1.1/4
        T['S4'][x+1] = C - RANGE * 1.1/2
        T['S5'][x+1] = (T['S4'][x+1]) - 1.168 * ((T['S3'][x+1]) - (T['S4'][x+1]))
        T['S6'][x+1] = 2*C - T['R6'][x+1]
   
    O = T['Open'][x+1]
    C = T['Close'][x+1]
    L = T['Low'][x+1]
    H = T['High'][x+1]
#     print(O, H, L, C)
    
    RANGE = H-L
    R3 = C + RANGE * 1.1/4
    R4 = C + RANGE * 1.1/2
    R6 = (H/L)*C
    R5 = R4 + 1.168 * (R4-R3)
    R4 = C + RANGE * 1.1/2

    PP = (H+L+C) / 3

#     S3 = C - RANGE * 1.1/4
#     S4 = C - RANGE * 1.1/2
#     S5 = (S4 - 1.168 * (S3-S4))
#     S6 = 2*C - R6
#     print(R6, R5, R4, R3, S3, S4, S5, S6)
    return T

resampled_data = ''
period = {'D':'Daily', 'W':'Weekly', 'M':'Monthly', 'Q':'Quarterly', 'Y':'Yearly'}
print("Periods", period)
choice = {1:'VIEW ALL Period Analyses', 2:'View Single Period Analysis'}
print('Choose',choice)
c = int(input())
if c == 2:
    p = input('Choose the period : ')
    if p in period:
        resampled_data = levels(data_resampling(nf, p))
        plot(resampled_data)
if c == 1:
    for p in period:
        resampled_data = levels(data_resampling(nf, p))
        plot(resampled_data)