import hkt_generator

import plotly.plotly
import plotly.graph_objs as go
from os import listdir

import markovify

#s = hook.HKTObject("data-files/polygon_dust.hkt")

#Load in all songs

#TODO
#Another folly, rythem repeats of one chord




#Creates a histogram of the all the chords in all the segments
#Uses a dictionary
#Also uses lambda expressions because yes
def createHistogram(songs, segFunc, varFunc):
    histogram = dict()

    for song in songs:
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
    plotly.offline.plot(fig, filename=output)


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

##TODO PROBLEM WITH MODES
def batchAnalyze(folder):
    songs = []
    artist = "Porter Robinson"

    for filename in listdir(folder):
        path = folder+"/"+filename
        new_song = hkt_generator.HKTObject(path)
        songs.append(new_song)

    num_songs = len(songs)
    total_distinct_chords = 0

    for song in songs:
        for segment in song.segments:
            for chord in segment.chords:
                total_distinct_chords+=1

    print(total_distinct_chords)

    getChords = lambda segment: segment.chords
    getChordsNoRest = lambda segment: segment.chordsNoRest

    getRoman = lambda chord: chord.roman
    getRomanBasic = lambda chord: chord.roman_basic

    getExtensions = lambda chord: chord.extension_disc

    #merge sus and emb chords
    getSus = lambda chord: chord.sus
    getEmb = lambda chord: chord.emb



    #HOW OFTEN EACH CHORD SHOWS UP
    full_chord_frequency = createHistogram(songs,getChordsNoRest,getRoman)
    basic_chord_frequency = createHistogram(songs,getChordsNoRest,getRomanBasic)
    extension_frequency = createHistogram(songs,getChordsNoRest,getExtensions)

    sus_frequency = createHistogram(songs,getChordsNoRest,getSus)
    emb_frequency = createHistogram(songs,getChordsNoRest,getEmb)

    total_emb_frequency = emb_frequency.copy()
    total_emb_frequency.update(sus_frequency)

    print(formatDic(basic_chord_frequency,total_distinct_chords, "Basic Chord Types"))
    print()
    print(formatDic(full_chord_frequency,total_distinct_chords, "Chord Types with Extensions"))
    print()
    print(formatDic(total_emb_frequency,total_distinct_chords, "Suspensions/Embellishments"))
    print()
    print(formatDic(extension_frequency,total_distinct_chords, "Extensions"))
    #print(chord_frequency)
    plotBarChartFromDict(basic_chord_frequency,"Basic Chord Types","basic")
    plotBarChartFromDict(full_chord_frequency,"Chord Types with Extensions","full")
    plotBarChartFromDict(total_emb_frequency,"Embellishments","emb")
    plotBarChartFromDict(extension_frequency,"Just Extensions","ext")
    #plotBarChartFromDict(total_emb_frequency)


    #MARKOV JUNK
    #DO THE MARKOV
    markovs = []
    for song in songs:
        text = ""
        if song.mode == "1":
            for segment in song.segments:
                for chord in segment.chordsNoRest:
                    text+=chord.roman_basic+" "
                    model = markovify.Text(text,state_size=1)
                    #markovs.append(model)

    #combo = markovify.combine(markovs)
    #for i in range(5):
        #print(combo.make_sentence())


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
