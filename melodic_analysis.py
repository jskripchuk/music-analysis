"""
melodic_analysis.py

Compiles all of the melodic data and places it in a Markov Model.
"""

import hkt_generator
import markovify
import statistics
import graphing
import tools
from random import random
from bisect import bisect
from os import listdir


def generate_markov_model(songs, model_state_size):
    """
    Takes in a list of HKT songs, and generates a combined markov model based
    off of the melodies in the songs.

    Args:
        songs: A list of HKT songs.
        model_state_size: How many instances the markov model should consider in a state

    Returns:
        A combined markov model build off of all the songs
    """
    markovs = []

    for song in songs:
        #For each song the melodic is put into a string
        #Each note is sperated by a space
        text = ""
        for segment in song.segments:
            for note in segment.melodyNoRest:
                text+=note.scale_degree+" "
        
        text = str(text)

        #We create a seperate model for every song and put them into a list
        if text != '':
            model = markovify.Text(text,state_size=model_state_size)
            markovs.append(model)

    #Then we combine all the models in the list
    combo = markovify.combine(markovs)
    return combo

def count_gestures_in_segment(segment, start, stop, gesture_rest_cutoff):
    number_of_gestures = 0

    first_note = True

    for note in segment.melody:
        if(note.isRest 
            and float(note.note_length) >= gesture_rest_cutoff
            and not first_note):
            
            if (float(note.start_measure) >= start
                and float(note.start_measure) <= stop):

                number_of_gestures+=1

        if first_note:
            first_note = False 

    return number_of_gestures

def count_gesture_type_in_segment(segment, gesture_rest_cutoff, reverse=False):

    #Looks at the last melody note in the list and determines what measure it starts on
    max_measure = int(segment.melody[-1].start_measure)

    first_four_bars = []
    second_four_bars = []
    eight_bars = []

    if(not reverse):
        for i in range(1,max_measure, 8):
            first_four_bars.append(count_gestures_in_segment(segment,i,i+3,gesture_rest_cutoff))
            second_four_bars.append(count_gestures_in_segment(segment,i+4,i+7,gesture_rest_cutoff))
            eight_bars.append(count_gestures_in_segment(segment,i,i+7,gesture_rest_cutoff))
    else:
        for i in range(max_measure, 1, -8):
            first_start = i-7
            first_stop = i-4
            second_start = i-3

            first_four_bars.append(count_gestures_in_segment(segment,first_start,first_stop,gesture_rest_cutoff))
            second_four_bars.append(count_gestures_in_segment(segment,second_start,i,gesture_rest_cutoff))
            eight_bars.append(count_gestures_in_segment(segment,first_start,i,gesture_rest_cutoff))
        
    
    first_four_bar_average = statistics.mean(first_four_bars)
    second_four_bar_average = statistics.mean(second_four_bars)
    eight_bar_average = statistics.mean(eight_bars)

    return[first_four_bar_average,second_four_bar_average,eight_bar_average]

def average_gestures_per_song(song, gesture_rest_cutoff, reverse=False):
    first_four_bars = []
    second_four_bars = []
    eight_bars = []

    for segment in song.segments:
        if len(segment.melody) != 0:
            result = count_gesture_type_in_segment(segment, gesture_rest_cutoff, reverse)
            first_four_bars.append(result[0])
            second_four_bars.append(result[1])
            eight_bars.append(result[2])

    if len(first_four_bars) != 0:
        first_four_bar_average = statistics.mean(first_four_bars)
    else:
        first_four_bar_average = 0

    if len(second_four_bars) != 0:
        second_four_bar_average = statistics.mean(second_four_bars)
    else:
        second_four_bar_average = 0

    if len(eight_bars) != 0:
        eight_bar_average = statistics.mean(eight_bars)
    else:
        eight_bar_average = 0

    return[first_four_bar_average,second_four_bar_average,eight_bar_average]

def average_gestures_in_corpus(songs, gesture_rest_cutoff, reverse=False):
    first_four_bars = []
    second_four_bars = []
    eight_bars = []

    for song in songs:
        if len(song.segments[0].melody) != 0:
            result = average_gestures_per_song(song, gesture_rest_cutoff, reverse)
            first_four_bars.append(result[0])
            second_four_bars.append(result[1])
            eight_bars.append(result[2])
        else:
            print("No Melody! Skipping song.")

    first_four_bar_average = statistics.mean(first_four_bars)
    second_four_bar_average = statistics.mean(second_four_bars)
    eight_bar_average = statistics.mean(eight_bars)

    return[first_four_bar_average,second_four_bar_average,eight_bar_average]

def generate_solfege_histogram(songs, filename):
    getMelodyNoRest = lambda segment: segment.melodyNoRest
    getScaleDegree = lambda note: note.scale_degree

    solfege= tools.createHistogram(songs,getMelodyNoRest,getScaleDegree)

    graphing.plotBarChartFromDict(solfege,"Solfege",filename+"_solfege")

def generate_rhythm_histogram(songs, filename):
    getMelodyNoRest = lambda segment: segment.melodyNoRest
    getRhythm = lambda note: note.note_length

    lengths = tools.createHistogram(songs, getMelodyNoRest, getRhythm)
    graphing.plotBarChartFromDict(lengths, "Melody Rhythms",filename+"_note_lengths")

class MelodicAnalysis:
    def __init__(self,songs,state_size):
        self.songs = songs
        self.markov_model = generate_markov_model(self.songs, state_size)

    def generate_line(self):
        return self.markov_model.make_sentence()

    def get_solfege_histogram(self, filename):
        generate_solfege_histogram(self.songs, filename)

    def get_note_length_histogram(self, filename):
        generate_rhythm_histogram(self.songs, filename)

    def get_gestures_in_corpus(self, gesture_cutoff, reverse=False):
        return average_gestures_in_corpus(self.songs, gesture_cutoff,reverse)
