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
                #print(note.scale_degree)
                text+=note.scale_degree+" "
        #text = "Hello dog aaa ffff ssss ffff"
        #text = "3 3 4 5 5 5 5 5 4 4 4 5 1 4 4 4 4 3 3 3 1 3 3 3 3 3 4 3 3 1 3 4 5 4 3 4 5 5 5 7 7 4 5 4 3 4 5 4 4 4 4 3 3 3 1 3 3 3 3 4 3 3 1"
        
        #Weird conversion here
        text = str(text)

        #We create a seperate model for every song and put them into a list

        #print(text)
        #text="A B C D E F G\n C D E F G E A G \n \n"
        if text != '':
            #print("AAA")
            #print(text)
            model = markovify.Text(text,state_size=model_state_size)
            markovs.append(model)

    #Then we combine all the models in the list
    combo = markovify.combine(markovs)
    #print(combo.make_sentence())

    return combo


#Problemo
#Gestures that are over the barline


#Gestures now take print(
#16 beats in 4 barsprint(
def count_gestures_in_segment(segment, start, stop, gesture_rest_cutoff):
    #print("SEG")
    number_of_gestures = 0

    first_note = True

    for note in segment.melody:
        #print("YO")
        if(note.isRest 
            and float(note.note_length) >= gesture_rest_cutoff
            and not first_note):
            


            #print("YO")
            if (float(note.start_measure) >= start
                and float(note.start_measure) <= stop):

                number_of_gestures+=1
        #else:
            #print(note.scale_degree)

        if first_note:
            first_note = False 
    #print("\n")
    return number_of_gestures
    
    #Used to make sure we don't include a rest at the beginning as a gesture
    #first_note = True
    #for note in segment.melody:
    #    if (note.isRest
    #        and float(note.note_length) > gesture_rest_cutoff
    #        and not first_note):
            #print(note.note_length)
            #TODO check if it works
    #        if (float(note.start_measure) >= start
    #            and float(note.start_measure) <= stop):

    #            number_of_gestures+=1

    #    if first_note:
    #        first_note = False

        #print(note.start_measure+": "+note.scale_degree)

    #return number_of_gestures

def count_gesture_type_in_segment(segment, gesture_rest_cutoff, reverse=False):
    max_measure = int(segment.melody[-1].start_measure)
    #print(max_measure)

    first_four_bars = []
    second_four_bars = []
    eight_bars = []
    #reverse = False
    #[0.13333333333333333, 0.18333333333333332, 0.31666666666666665]
    #[0.05, 0.26666666666666666, 0.31666666666666665]
    if(not reverse):
        for i in range(1,max_measure, 8):
            #print(((i,i+3),(i+4,i+7),(i,i+7)))
            first_four_bars.append(count_gestures_in_segment(segment,i,i+3,gesture_rest_cutoff))
            second_four_bars.append(count_gestures_in_segment(segment,i+4,i+7,gesture_rest_cutoff))
            eight_bars.append(count_gestures_in_segment(segment,i,i+7,gesture_rest_cutoff))
        #print("#############")
    else:
        for i in range(max_measure, 1, -8):
            first_start = i-7
            first_stop = i-4
            second_start = i-3

            #print(((first_start, first_stop),(second_start,i),(first_start,i)))
            first_four_bars.append(count_gestures_in_segment(segment,first_start,first_stop,gesture_rest_cutoff))
            second_four_bars.append(count_gestures_in_segment(segment,second_start,i,gesture_rest_cutoff))
            eight_bars.append(count_gestures_in_segment(segment,first_start,i,gesture_rest_cutoff))
        #print("##############")
        #print("Nut")
        #print([first_four_bars,second_four_bars,eight_bars])
    
    #first_four_bars = count_gestures_in_segment(segment,1,4,gesture_rest_cutoff)
    #print("DONE")
    #second_four_bars = count_gestures_in_segment(segment,5,8,gesture_rest_cutoff)
    #print("DONE")
    #eight_bars = count_gestures_in_segment(segment,1,8,gesture_rest_cutoff)
    #print(first_four_bars)
    #print(second_four_bars)
    #print(eight_bars)
    #print()
    
    first_four_bar_average = statistics.mean(first_four_bars)
    second_four_bar_average = statistics.mean(second_four_bars)
    eight_bar_average = statistics.mean(eight_bars)

    #print((first_four_bar_average, second_four_bar_average, eight_bar_average))
    #print("///////////////////")

    return[first_four_bar_average,second_four_bar_average,eight_bar_average]
    #return [first_four_bars,second_four_bars,eight_bars]

###TODO: CHECK IF THE SONG ACTUALLY HAS A MELODY YA DINUGS
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

    if len(eight_bars) == 0:
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
        #self.gesture_rest_cutoff = gesture_rest_cutoff
        #self.gestures_in_corpus = average_gestures_in_corpus(self.songs, gesture_rest_cutoff)
        #generate_solfege_histogram(self.songs)
        #print(average_gestures_per_song(self.songs[0],gesture_rest_cutoff))
        self.markov_model = generate_markov_model(self.songs, state_size)
        #print(self.markov_model.make_sentence())
        #print(count_gesture_type_in_segment(self.songs[0].segments[0],gesture_rest_cutoff))

    def generate_line(self):
        return self.markov_model.make_sentence()

    def get_solfege_histogram(self, filename):
        generate_solfege_histogram(self.songs, filename)

    def get_note_length_histogram(self, filename):
        generate_rhythm_histogram(self.songs, filename)

    def get_gestures_in_corpus(self, gesture_cutoff, reverse=False):
        return average_gestures_in_corpus(self.songs, gesture_cutoff,reverse)
