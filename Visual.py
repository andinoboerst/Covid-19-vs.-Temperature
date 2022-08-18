import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import datetime
from scipy.ndimage.filters import gaussian_filter1d
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.lines import Line2D
from matplotlib.widgets import TextBox
import os

def prepare_data():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '/covid_countries.csv')
    df = pd.read_csv(filename)

    df['date'] = pd.to_datetime(df.loc[:,'date'])
    df['country_name'] = df['country_name'].str.lower()
    df.loc[:,~df.columns.isin(['date', 'country_name'])] = df.loc[:,~df.columns.isin(['date', 'country_name'])].apply(pd.to_numeric)
    df.loc[:,'perc_new_confirmed'] = df.loc[:,'new_confirmed'] / df.loc[:,'population']

    country_list = df.loc[:,'country_name'].unique()

    return df, country_list

def extract_data(df, country):
    df_country = df.loc[df['country_name'] == country.lower()].copy()
    df_country.loc[:,~df_country.columns.isin(['date', 'country_name'])] = df_country.loc[:,~df.columns.isin(['date', 'country_name'])].fillna(method='ffill')

    x_country = df_country.loc[:,'date'].tolist().copy()
    y_country_cases = gaussian_filter1d(df_country.loc[:,'perc_new_confirmed'], sigma=2)
    y_country_temps = gaussian_filter1d(df_country.loc[:,'average_temperature_celsius'], sigma=2)

    return x_country, y_country_cases, y_country_temps

def plot_data(ax1,ax2,country,x_country,y_country_cases,y_country_temps):
    ax1.cla()
    ax2.cla()
    cases_threshold = 0.0002
    cases_country, = ax2.plot(x_country, y_country_cases, linestyle='-', color = 'darkgreen')
    ax2.set_ylabel('New cases as % of Population')
    ax1.set_ylabel('Avg. Temperature [Celsius]')

    x_min, x_max = ax2.get_xlim()

    mask_threshold = y_country_cases>=cases_threshold

    line_threshold = ax2.hlines(cases_threshold, x_min, x_max, color='grey')

    ax2.fill_between(x_country, y_country_cases, y2=cases_threshold, where=mask_threshold, facecolor='firebrick', alpha=0.35)
    ax2.fill_between(x_country, y_country_cases, y2=cases_threshold, where=~mask_threshold, facecolor='cornflowerblue', alpha=0.35)

    # plot temperature

    points = np.array([x_country, y_country_temps]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    segments[:, :, 0] = mdates.date2num(segments[:, :, 0])


    mask_line = np.zeros(len(segments))
    mask_line[mask_threshold[:-1]] = 1
    cmap = ListedColormap(['cornflowerblue', 'firebrick'])
    norm = BoundaryNorm([0, 0.5, 1], cmap.N)
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(mask_line)
    line_temps = ax1.add_collection(lc)

    ax1.set_ylim([min(y_country_temps)-2, max(y_country_temps)+2])

    proxies = [Line2D([0, 1], [0, 1], color='firebrick'), Line2D([0, 1], [0, 1], color='cornflowerblue')]
    ax1.legend(handles=proxies, labels = [f'New cases above threshold', 'New cases below threshold'], loc='upper left')


    fig.suptitle(f'Correlation between Temperature and New Covid Cases in {country}')

    # Take care of the x-axis

    for tick in ax1.xaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_horizontalalignment('center')

    ax2.set_xlim([datetime.date(2020, 1, 1), datetime.date(2021, 12, 31)])

    ax2.xaxis.set_minor_locator(mdates.MonthLocator(bymonthday=16))
    # '%b' to get the names of the month
    ax2.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator())
    ax2.xaxis.set_major_formatter(ticker.NullFormatter())

    # fontsize for month labels
    ax2.tick_params(labelsize=10, which='both')
    # create a second x-axis beneath the first x-axis to show the year in YYYY format
    sec_xaxis = ax2.secondary_xaxis(-0.08)
    sec_xaxis.xaxis.set_minor_locator(mdates.YearLocator(1, month=7, day=1))
    sec_xaxis.xaxis.set_major_locator(mdates.YearLocator())
    sec_xaxis.xaxis.set_major_formatter(ticker.NullFormatter())
    sec_xaxis.xaxis.set_minor_formatter(mdates.DateFormatter('%Y'))

    for tick in ax2.xaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_horizontalalignment('center')

    for tick in sec_xaxis.xaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_horizontalalignment('center')


def submit(text):
    new_country = text.lower()
    if new_country in country_list:
        ax1.set_title('')
        new_x_country, new_y_country_cases, new_y_country_temps = extract_data(df,new_country)
        plot_data(ax1,ax2,new_country,new_x_country, new_y_country_cases, new_y_country_temps)
        plt.draw()
    else:
        ax1.set_title(f'{new_country} is not a valid entry.', color='r')
        plt.draw()

country = "Spain"

df, country_list = prepare_data()
x_country, y_country_cases, y_country_temps = extract_data(df,country)

# plot results

fig = plt.figure()
gs = fig.add_gridspec(2, hspace=0)
(ax1,ax2) = gs.subplots(sharex=True)

plot_data(ax1,ax2,country,x_country,y_country_cases,y_country_temps)

axbox = plt.axes([0.1, 0.9, 0.24, 0.05])
text_box = TextBox(axbox, 'Country', initial=country)
text_box.on_submit(submit)

plt.show()




