#run as
#python3 <input_file> <output_file>

import sys
import plotly
import plotly.graph_objs as go

filename = sys.argv[1]
saveas = sys.argv[2]
print(filename)
file_object = open(filename, "r")
file_text = file_object.read().split()
data = [go.Histogram(x=file_text)]

plotly.offline.plot(data, filename="graphs/"+saveas, auto_open=False)