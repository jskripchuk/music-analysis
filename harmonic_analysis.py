import hook

import plotly.plotly
import plotly.graph_objs as go
from os import listdir

import markovify

#s = hook.HKTObject("data-files/polygon_dust.hkt")

#Load in all songs




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



def diatonicVsNondiatonic(song):
    vs = {"Diatonic": 0, "Nondiatonic": 0}

    for segment in song.segments:
        for chord in segment.chords:
            if chord.borrowed == None:
                vs["Diatonic"]+=1
            else:
                vs["Nondiatonic"]+=1


    print(vs)

#def generateGraphs():
    #plotBarChart()

def plotBarChartFromDict(dic):
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


def analyzeHarmony(song):
    #chord_histogram = createChordHistogram(s)
    getChords = lambda segment: segment.chords
    getChordsNoRest = lambda segment: segment.chordsNoRest

    getRoman = lambda chord: chord.roman
    getExtensions = lambda chord: chord.extension_disc
    getSus = lambda chord: chord.sus


    #HOW OFTEN EACH CHORD SHOWS UP
    chord_frequency = createHistogram(song,getChords,getRoman)
    #HOW OFTEN EACH TYPE OF EXTENSION SHOWS UP
    #extension_frequency = createHistogram(s,getChords,getExtensions)
    #suspension_frequency = createHistogram(s,getChords,getSus)

    #plotBarChartFromDict(suspension_frequency)
    #DIATONIC VS NON-DIATONIC CHORDS
    #diatonicVsNondiatonic(song)

    plotBarChartFromDict(chord_frequency)



##TODO PROBLEM WITH MODES
def batchAnalyze(folder):
    songs = []
    for filename in listdir(folder):
        path = folder+"/"+filename
        new_song = hook.HKTObject(path)
        songs.append(new_song)

    #DO THE MARKOV
    markovs = []
    for song in songs:
        text = ""
        if song.mode == "1":
            for segment in song.segments:
                for chord in segment.chordsNoRest:
                    text+=chord.roman_basic+" "
                    model = markovify.Text(text,state_size=1)
                    markovs.append(model)

    combo = markovify.combine(markovs)
    for i in range(5):
        print(combo.make_sentence())


    #print(songs)
        #print(path)

batchAnalyze("data-files/porter_robinson")

#analyzeHarmony(s)
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
