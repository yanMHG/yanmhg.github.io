from plotly.graph_objects import Scatter
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import pandas as pd

def get_matplotlib_range(data_1d):
    fig = plt.figure()
    plt.plot(data_1d)
    return list(plt.gca().get_ylim())

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
