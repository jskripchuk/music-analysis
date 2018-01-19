import plotly.plotly
import plotly.graph_objs as go

def plotBarChartFromDict(dic,title,output):
    plotBarChart(list(dic.keys()), list(dic.values()), title,output)

def plotBarChart(x_data, y_data,tit,output):
    layout_comp = go.Layout(
        title = tit,
        xaxis=dict(
            title = "Chords",
            type = "category"
        )
    )
    data_comp = [go.Bar(
            x= x_data,
            y= y_data
    )]

    fig = go.Figure(data = data_comp, layout=layout_comp)
    plotly.offline.plot(fig, filename="graphs/"+output)

def formatDic(dic, total,disc):
    output="["+disc+"]\n"
    output+="##########\n"
    first = True

    for key in dic:
        val = dic[key]
        #rounds to two decimal places
        ratio = (val/total)*100
        form = "{0:.2f}".format(ratio)
        if key != None:
            if not first:
                output+="\n"
            output+=key+": "+str(val)+" ["+str(form)+"%]"
        first = False

    output+="\n##########"
    return output
