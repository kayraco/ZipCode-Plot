import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Select
from bokeh.layouts import column
import os.path as osp

script_dir = osp.dirname(__file__)
src_file = osp.join(script_dir, '..', 'avg_monthly_times.csv')
df = pd.read_csv(src_file)

zipcodes = df.iloc[:, 0]
zipcodes = (str(x) for x in zipcodes)
zipcodes = sorted(list(zipcodes))
zipcodes.remove(str(2020))
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]
z1 = Select(title="Choose Zipcode 1", options=zipcodes, value=zipcodes[0])
z2 = Select(title="Choose Zipcode 2", options=zipcodes, value=zipcodes[1])

x = list(i + 1 for i in range(9))  # 1-9
y = df.loc[236, :].values.tolist()
y.remove(2020)

y1 = df.loc[df['Zipcode'] == 10000].values.flatten().tolist()
y1.remove(10000.0)
y2 = df.loc[df['Zipcode'] == 10001].values.flatten().tolist()
y2.remove(10001.0)

ds = ColumnDataSource(data={'x': months, 'y': y, 'y2': y2, 'y1': y1})

all_p = figure(x_range=months, y_range=(0, 200),
               x_axis_label='Months', y_axis_label='Response Time in Hours')
# x_range=months gives month x-axis tickers
all_p.line(x='x', y='y', line_width=2, line_color='gray', legend_label='All Zipcodes', source=ds)
all_p.line(x='x', y='y1', line_width=2, line_color='red', legend_label='Zipcode 1', source=ds)
all_p.line(x='x', y='y2', line_width=2, line_color='blue', legend_label='Zipcode 2', source=ds)


def change_zip1(attr, old, new):  # update zip1
    zip1 = float(z1.value)
    temp_y = df.loc[df['Zipcode'] == zip1].values.flatten().tolist()
    temp_y.remove(zip1)
    ds.data = {'x': months, 'y1': temp_y, 'y2': y2, 'y': y}


def change_zip2(attr, old, new):  # update zip2
    zip2 = float(z2.value)
    temp_y = df.loc[df['Zipcode'] == zip2].values.flatten().tolist()
    temp_y.remove(zip2)
    ds.data = {'x': months, 'y': y, 'y1': y1, 'y2': temp_y}


z1.on_change('value', change_zip1)
z2.on_change('value', change_zip2)

layout = column(z1, z2, all_p)
curdoc().add_root(layout)
