import hook

import plotly.plotly
import plotly.graph_objs as go

s = hook.HKTObject("data-files/tennis.hkt")



#Creates a histogram of the all the chords in all the segments
#Uses a dictionary
#Also uses lambda expressions because yes
def createHistogram(song, segFunc, varFunc):
    histogram = dict()

    for segment in song.segments:
        for obj in segFunc(segment):
            inHisto = False

            for key in histogram:
                if varFunc(obj) == key:
                    histogram[key]+=1
                    inHisto = True
                    break

            if not inHisto:
                histogram[varFunc(obj)] = 1

    return histogram
#extensions


def analyzeHarmony(song):
    #chord_histogram = createChordHistogram(s)
    getChords = lambda segment: segment.chords

    getRoman = lambda chord: chord.roman
    getExtensions = lambda chord: chord.extension_disc

    chord_frequency = createHistogram(s,getChords,getRoman)
    extension_frequency = createHistogram(s,getChords,getExtensions)
    #print(createHistogram(s,getChords,extension_disc))
    plotBarChartFromDict(extension_frequency)
    #generateGraphs(chord_histogram)
    #print(chord_histogram)

#def generateGraphs():
    #plotBarChart()

def plotBarChartFromDict(dic):
    #print(list(dic.keys()))
    #print(list(dic.values()))
    #plotBarChart(["7","3","2"],[2,5,1])
    plotBarChart(list(dic.keys()), list(dic.values()))

def plotBarChart(x_data, y_data):
    layout_comp = go.Layout(
        title = "Chord Stuff",
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
    plotly.offline.plot(fig, filename='basic-bar')

analyzeHarmony(s)
#for key in chord_histogram:
    #print(key)

        #print(chord.roman)

#for key in chord_histogram:

    #print(key)

#CHORD TYPES
#-What chords do we have? (Histogram)\
#-What function are they? (Tonic/Dom/Subdom
#-Non diatonic?
#-Extensions?
#RHYTHM
#Syncopation? Anticipation?
#How long do they last?
#Evenly spaced
#OTHER
#Bass movement by intervals?
