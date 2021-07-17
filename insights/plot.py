from plotly.graph_objects import Scatter
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import sqlite3

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def update_csv_files(flw_out, reach_out):
    # Read stuff from database
    db_fn = sys.argv[1]
    cmd = "sqlite3 %s << EOF > %s\n" % (db_fn, flw_out)
    cmd += '.mode csv\n'
    cmd += '.separator ","\n'
    cmd += '.out %s\n' % (flw_out)
    cmd += 'SELECT day, value FROM human WHERE time = "22:00" ORDER BY day\n'
    cmd += 'EOF'
    os.system(cmd)
    cmd = "sqlite3 %s << EOF > %s\n" % (db_fn, reach_out)
    cmd += '.mode csv\n'
    cmd += '.separator ","\n'
    cmd += '.out %s\n' % (reach_out)
    cmd += 'SELECT date, reach FROM insights ORDER BY date\n'
    os.system(cmd)
    line_prepender(flw_out, "Data,Seguidores")
    line_prepender(reach_out, "Data,Alcance")
    # 

def get_matplotlib_range(data_1d):
    fig = plt.figure()
    plt.plot(data_1d)
    return list(plt.gca().get_ylim())

flw_out = 'data/followers.csv'
reach_out = 'data/reach.csv'

update_csv_files(flw_out, reach_out)

seg = pd.read_csv('data/followers.csv')
alc = pd.read_csv('data/reach.csv')

xrange_limit = 30 * 8 # Otherwise there are too many points in the figure

all = pd.merge(seg, alc, on='Data').tail(xrange_limit)

fig = make_subplots(2, 1,
                    vertical_spacing=.1,
                    shared_xaxes=True,
                    subplot_titles=("Seguidores", "Alcance"))

for i, lab in enumerate(["Seguidores", "Alcance"]):
    fig.add_trace(Scatter(x=all["Data"], y=all[lab],
                          name=lab,
                          mode="lines+markers",
                          fill='tonexty'),
                      row=i+1, col=1)
    fig.update_yaxes(range=get_matplotlib_range(all[lab]),
                     row=i+1,
                     col=1)


fig.update_layout(showlegend=False)

fig.write_html("../ac-yoga-insights.html")
