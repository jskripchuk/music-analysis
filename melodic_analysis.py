import hkt_generator
import markovify
import statistics
import graphing
import tools
from random import random
from bisect import bisect
from os import listdir


def generate_markov_model(songs, model_state_size):
    markovs = []

    for song in songs:
        #For each song the melodic is put into a string
        #Each note is sperated by a space
        text = ""
        for segment in song.segments:
            for note in segment.melodyNoRest:
                text+=note.scale_degree+" "

        #We create a seperate model for every song and put them into a list

        #print(text)
        #text="A B C D E F G\n C D E F G E A G \n \n"
        if text != '':
            model = markovify.Text(text,state_size=model_state_size)
            markovs.append(model)

    #Then we combine all the models in the list
    combo = markovify.combine(markovs)

    return combo


#Problemo
#Gestures that are over the barline

def count_gestures_in_segment(segment, start, stop, gesture_rest_cutoff):
    number_of_gestures = 0

    #Used to make sure we don't include a rest at the beginning as a gesture
    first_note = True
    for note in segment.melody:
        if (note.scale_degree == "rest"
            and float(note.note_length) > gesture_rest_cutoff
            and not first_note):
            #print(note.note_length)
            #TODO check if it works
            if (float(note.start_measure) >= start
                and float(note.start_measure) <= stop):

                number_of_gestures+=1

        if first_note:
            first_note = False

        #print(note.start_measure+": "+note.scale_degree)

    if len(segment.melody) != 0 and stop == 8:
        if segment.melody[len(segment.melody)-1].scale_degree != "rest":
            number_of_gestures+=1

    return number_of_gestures

def count_gesture_type_in_segment(segment, gesture_rest_cutoff):
    first_four_bars = count_gestures_in_segment(segment,1,4,gesture_rest_cutoff)
    #print("DONE")
    second_four_bars = count_gestures_in_segment(segment,5,8,gesture_rest_cutoff)
    #print("DONE")
    eight_bars = count_gestures_in_segment(segment,1,8,gesture_rest_cutoff)

    return [first_four_bars,second_four_bars,eight_bars]

def average_gestures_per_song(song, gesture_rest_cutoff):
    first_four_bars = []
    second_four_bars = []
    eight_bars = []

    for segment in song.segments:
        result = count_gesture_type_in_segment(segment, gesture_rest_cutoff)
        first_four_bars.append(result[0])
        second_four_bars.append(result[1])
        eight_bars.append(result[2])

    first_four_bar_average = statistics.mean(first_four_bars)
    second_four_bar_average = statistics.mean(second_four_bars)
    eight_bar_average = statistics.mean(eight_bars)

    return[first_four_bar_average,second_four_bar_average,eight_bar_average]

def average_gestures_in_corpus(songs, gesture_rest_cutoff):
    first_four_bars = []
    second_four_bars = []
    eight_bars = []

    for song in songs:
        result = average_gestures_per_song(song, gesture_rest_cutoff)
        first_four_bars.append(result[0])
        second_four_bars.append(result[1])
        eight_bars.append(result[2])

    first_four_bar_average = statistics.mean(first_four_bars)
    second_four_bar_average = statistics.mean(second_four_bars)
    eight_bar_average = statistics.mean(eight_bars)

    return[first_four_bar_average,second_four_bar_average,eight_bar_average]

def generate_solfege_histogram(songs):
    getMelodyNoRest = lambda segment: segment.melodyNoRest
    getScaleDegree = lambda note: note.scale_degree

    solfege= tools.createHistogram(songs,getMelodyNoRest,getScaleDegree)

    graphing.plotBarChartFromDict(solfege,"Solfege","solfege")


class MelodicAnalysis:
    def __init__(self,songs,state_size,gesture_rest_cutoff):
        self.songs = songs
        self.gestures_in_corpus = average_gestures_in_corpus(self.songs, gesture_rest_cutoff)
        #generate_solfege_histogram(self.songs)
        #print(average_gestures_per_song(self.songs[0],gesture_rest_cutoff))
        self.markov_model = generate_markov_model(self.songs, state_size)
        #print(count_gesture_type_in_segment(self.songs[0].segments[0],gesture_rest_cutoff))

    def generate_line(self):
        return self.markov_model.make_sentence()

    def generate_solfege_histogram(self):
        self.generate_solfege_histogram(self.songs)

    def get_gestures_in_corpus(self):
        return self.gestures_in_corpus
