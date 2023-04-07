import pandas as pd
import numpy as np


## this part is just combining the datasets I'm using for "drunk driving
## related accidents" data.
## in 2010-2021 I just use the "dimpair.csv" (with varying cases depending on the year)
## and pull out the "DRIMPAIRNAME" variable and count the number of occurrences of
## "Under the Influence of Alcohol, Drugs, or Medication."
## for 1996-2009 it seems I just take the "ACCIDENT.CSV" file and count the number
## of occurrences of the "DRUNK_DR" variable being equal to 1.
"""
final_data = pd.DataFrame(data={'Year':range(1996,2022)})
index = 0
for year in range(1996, 2022):
    if 1996 <= year <= 2014:
        data = pd.read_csv('ACCIDENT{0}.CSV'.format(year))
        num_drunk_dr = len(data[data['DRUNK_DR']==1].reset_index(drop=True))
        final_data.loc[index,'Number of Drunk Driving Accidents'] = num_drunk_dr
    elif 2015 <= year <= 2019:
        data = pd.read_csv('DrImpair{0}.CSV'.format(year))
        num_drunk_dr = len(data[data['DRIMPAIRNAME']=='Under the Influence of Alcohol, Drugs or Medication'].reset_index(drop=True))
        print(num_drunk_dr)
        final_data.loc[index, 'Number of Drunk Driving Accidents'] = num_drunk_dr
    elif 2020 <= year <= 2021:
        data = pd.read_csv('drimpair{0}.csv'.format(year))
        num_drunk_dr = len(data[data['DRIMPAIRNAME']=='Under the Influence of Alcohol, Drugs or Medication'].reset_index(drop=True))
        print(num_drunk_dr)
        final_data.loc[index, 'Number of Drunk Driving Accidents'] = num_drunk_dr
    index += 1
    print(year,'\n',final_data,'\n\n')

final_data.to_csv('drunk-driving-accidents.csv',index=False)
"""

## now need to get all the price data for the wine companies and make it into one time series dataset
"""
constellation = pd.read_csv('STZ.csv')
brown_forman = pd.read_csv('BF-B.csv')
diageo = pd.read_csv('DEO.csv')
willamette = pd.read_csv('WVVI.csv')

wines = {
    'Constellation':constellation,
    'Brown-Forman':brown_forman,
    'Diageo':diageo,
    'Willamette':willamette
}
final_wine_data = pd.DataFrame(data={'Year':range(1996,2022)})
for wine in wines.keys():
    index = 0
    wine_data = wines[wine]
    for year in range(1996, 2022):
        print(year, wine)
        data = wine_data[wine_data['Date'].str.contains(str(year))].reset_index(drop=True)
        #print(data)
        ann_return = np.log(data['Open'][len(data)-1] / data['Close'][0])
        #print(ann_return)
        final_wine_data.loc[index, '{0} Annual Return'.format(wine)] = ann_return
        index += 1
        print(final_wine_data, '\n\n')

for row in range(len(final_wine_data)):
    data = final_wine_data.loc[row,final_wine_data.columns != 'Year']
    final_wine_data.loc[row, 'Average Annual Return'] = np.mean(data)
    print(final_wine_data)


final_wine_data.to_csv('wine-returns.csv',index=False)
"""

## now, as a final step (or maybe second to last step), let's make my life marginally easier
## and take the average price over each year (since we currently have monthly data)
"""
prices = pd.read_csv('city-wine-price.csv')

final_price_data = pd.DataFrame(data={'Year':range(1996,2022)})
index = 0
for year in range(1996, 2022):
    print(year)
    price_data = prices[prices['Year']==year]['Value'].reset_index(drop=True)
    avg_price = np.mean(price_data)
    final_price_data.loc[index, 'Average Annual Price'] = avg_price
    index += 1
    print(final_price_data, '\n\n')

final_price_data.to_csv('avg-annual-prices.csv',index=False)
"""

## ...turns out the plot with a slider needs to be done in python. Worry not!... this is python!

## first bring in the data and combine it into one dataframe

prices = pd.read_csv('avg-annual-prices.csv')
returns = pd.read_csv('wine-returns.csv')
accidents = pd.read_csv('drunk-driving-accidents.csv')

data = prices.join([returns[['Average Annual Return']], accidents[['Number of Drunk Driving Accidents']]])
data.loc[len(data),'Year'] = 2022
data.loc[len(data)+1,'Year'] = 2023
#data['Factor'] = range(1, len(data))

import plotly.graph_objects as go

fig1 = go.Figure()

for step in np.arange(-0.05, 0.06, 0.01):
    fig1.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color='#00CED1',width=6),
            name='𝜈 = ' + str(step),
            x=data['Year'],
            ## this is where I use the coefficients from the VaR model to spit out an estimate
            ## for returns/accidents... I think
            ## first let's do returns
            y=( ((1+step) * -0.009074 * data['Average Annual Price'].shift(1)) + (-0.01465 * data['Average Annual Return'].shift(1)) +
                (-0.00001658 * data['Number of Drunk Driving Accidents'].shift(1)) + 0.3373)
        )
    )

#fig.data[10].visible = True

steps = []
for i in range(len(fig1.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig1.data)},
              {"title": "Average Annual Wine Industry Returns; {0}% Wine tax".format(str(i-5))}]  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=10,
    #currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)]

fig1.update_layout(
    sliders=sliders,
    yaxis_range=[0.055, 0.1475]
)
#import plotly
#plotly.offline.plot(fig1, filename = 'plot_test.html', auto_open=False)
fig1.write_html('plot.html',auto_open=True)


#import chart_studio.plotly as py
#py.plot(fig1, filename='wine-returns', auto_open=True)

"""
fig2 = go.Figure()

for step in np.arange(-0.05, 0.06, 0.01):
    fig2.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color='#00CED2',width=6),
            name='𝜈 = ' + str(step),
            x=data['Year'],
            ## now let's do number of drunk driving accidents
            y=( ((1+step) * -271.9583 * data['Average Annual Price'].shift(1)) + (889.4117 * data['Average Annual Return'].shift(1)) +
                (0.6852 * data['Number of Drunk Driving Accidents'].shift(1)) + 5127.2436)
        )
    )

#fig.data[10].visible = True

steps = []
for i in range(len(fig2.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig2.data)},
              {"title": "Average Annual Impaired Driving Accidents; {0}% Wine tax".format(str(i-5))}]  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=10,
    #currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)]

fig2.update_layout(
    sliders=sliders,
    yaxis_range=[5000, 12000]
)

fig2.write_html('plot.html',auto_open=True)


"""