#run as
#python3 <input_file> <output_file>

import sys
import plotly
import plotly.graph_objs as go

filename = sys.argv[1]
saveas = sys.argv[2]

file_object = open(filename, "r")
file_text = file_object.read().split()
file_text = sorted([int(i) for i in file_text])
data = [go.Histogram(x=file_text, xbins=go.histogram.XBins(start=0,
                                   end=300,
                                   size=5))]

plotly.offline.plot(data, filename="graphs/"+saveas, auto_open=False)
