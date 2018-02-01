import hkt_generator
import statistics
import markovify
import graphing
import tools
from random import random
from bisect import bisect
from os import listdir

def createHistogram(songs, segFunc, varFunc):
    """
    Taks in a list of songs, and creates a histogram (dictionary)
    based on the qualities desired with the lambda functions segFunc and varFunc.

    Args:
        songs (list of HKTObject): A list of all songs to be analyzed
        segFunc (lambda): A function that returns the part of a segment
            in HKTObject. (Either the chords or the melody)
        varFunc (lambda): A function that returns the quality of the item that
            we wish to make a histogram out of.
            (Eg. Roman Numeral, seventh quality, suspension...)

    Returns:
        A dictionary that contains a tally of how many times a certain quality
        occurs in the specified part of the segment. For example:

        Progression: I-IV-I-V
        hist["I"] = 2
        hist["IV"] = 1
        hist["V"] = 1
    """

    histogram = dict()

    for song in songs:
        for segment in song.segments:
            for obj in segFunc(segment):
                inHisto = False

                #If it is in the histogram, then increment the tally
                for key in histogram:
                    if varFunc(obj) == key:
                        histogram[key]+=1
                        inHisto = True
                        break

                #If it is not in the histogram, then add it and tally it
                if not inHisto:
                    histogram[varFunc(obj)] = 1

    return histogram

def weighted_choice(choices):
    """
    Taks in a list of 2-tuples of the form (Item,numberOfOccurences), and
    selects an item from the list randomly, but weighted resepect to the
    number of occurences.

    Args:
        choices (list of 2-tuples): A list of 2-tuples to be chosen from

    Returns:
        An item from the 2-tuple, randomly chosen but weighted respect to
        the number of times it occurs

    Code from Raymond Hettinger
    https://stackoverflow.com/a/4322940
    """

    values, weights = zip(*choices)
    total = 0
    cum_weights = []

    for w in weights:
        total += w
        cum_weights.append(total)

    x = random() * total
    i = bisect(cum_weights, x)

    return values[i]

def get_corpus_list(folder):
    """
    Gets the corpus as a song array
    """
    songs = []

    for filename in listdir(folder):
        path = folder+"/"+filename
        new_song = hkt_generator.HKTObject(path)
        songs.append(new_song)

    return songs

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
