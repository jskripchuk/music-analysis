import hkt_generator
import statistics
import markovify
import graphing
import tools
from random import random
from bisect import bisect
from os import listdir

"""
harmonic_analysis.py

Takes the Hooktheory corpus of an artist and performs a statistical analysis,
of the harmony. Also creates a markov model that can generate a harmonic
progression and rhythm.

"""


def calculate_statistics(songs, filename):
    """
    Calulates various statistics based on a Hooktheory corpus, and generates
    multiple graphs and bar charts.

    Args:
        songs (list of HKTObject): A list HKTObjects representing the corpus

    Returns:
        Nothing
    """

    #Lambda functions used to create histograms
    getChords = lambda segment: segment.chords
    getChordsNoRest = lambda segment: segment.chordsNoRest

    getRoman = lambda chord: chord.roman
    getRomanBasic = lambda chord: chord.roman_basic

    getSus = lambda chord: chord.susString
    getEmb = lambda chord: chord.emb
    getAdds = lambda chord: chord.addsString

    #Create histograms
    #full_chord_frequency = tools.createHistogram(songs,getChordsNoRest,getRoman)
    #basic_chord_frequency = tools.createHistogram(songs,getChordsNoRest,getRomanBasic)
    #extension_frequency = tools.createHistogram(songs,getChordsNoRest,getExtensions)

    #Merge sus and emb chords into one graph
    sus_frequency = tools.createHistogram(songs,getChordsNoRest, getSus)
    extension_frequency = tools.createHistogram(songs,getChordsNoRest,getEmb)
    adds_frequency = tools.createHistogram(songs,getChordsNoRest, getAdds)

    #total_sus_frequency = sus_frequency.copy()
    #total_sus_frequency.update(adds_frequency)

    #Generate graphs
    #graphing.plotBarChartFromDict(basic_chord_frequency,"Basic Chord Types","basic_roman_numerals")
    #graphing.plotBarChartFromDict(full_chord_frequency,"Chord Types with Extensions","full_roman_numerals")
    graphing.plotBarChartFromDict(adds_frequency, "Additions", filename+"_additions")
    graphing.plotBarChartFromDict(sus_frequency,"Suspensions",filename+"_suspensions")
    graphing.plotBarChartFromDict(extension_frequency,"Just Extensions",filename+"_extensions")

#def get_average_tempo(songs):
    

def generate_markov_model(songs, model_state_size):
    """
    Generates a harmonic markov model based off of all the hooktheory songs
    given

    Args:
        songs (list of HKTObject): A list HKTObjects representing the corpus
        model_state_size (int): The state size that should be used for the model

    Returns:
        A markov model that represents the entire harmonic corpus given
    """

    markovs = []

    for song in songs:
        #For each song the harmonic progression is put into a string
        #Each chord is sperated by a space
        text = ""
        for segment in song.segments:
            #print(segment)
            for chord in segment.chordsNoRest:
                #print(chord)
                text+=chord.roman_basic+" "
                #print(chord.roman_basic)

        #Weird conversion here
        text = str(text)

        #We create a seperate model for every song and put them into a list
        if text != '':
            #print("Text: "+text)
            model = markovify.Text(text,state_size=model_state_size)
            markovs.append(model)

    #Then we combine all the models in the list
    #print(markovs)

    #print(markovs)
    combo = markovify.combine(markovs)

    return combo


def generate_rhythm_pattern(rhythm_prob, chords_per_measure):
    """
    Generates a rhythm pattern based of the "hit-vector" given.

    Args:
        rhythm_prob (list of ints [size=8]): A list where each index contains
            how many times a chord started on that index.

    Returns:
        An array that contains a rhythmic pattern, where 0 is no hit and 1 is
        a hit. This array represents one segment of a song.
    """
    #print(rhythm_prob)
    #TODO
    #Account for time signatures other than 4/4
    #Add ability to skip measures or add more than one hit per measures,
    #based off of the corpus

    #1 Segment = 8 measures
    #1 Measure = 8 beats
    #8*8=64 beats per segment
    beats_per_segment = 64
    generated_rhythm_array = [0]*beats_per_segment
    #Always hit on the first beat (for now)
    generated_rhythm_array[0]=1


    #Flesh out the rest based on probability
    for i in range(0,8):
        rhythm_copy = list(rhythm_prob)
        chords_this_measure = tools.weighted_choice(chords_per_measure)

        #Generate how ever many chords we have to
        for j in range(0, chords_this_measure):
            #Figure out what beat to place them on
            start_beat = tools.weighted_choice(rhythm_copy)
            beat_to_place = (i*8)+start_beat

            #shouldn't be greater than 64
            if beat_to_place < 64:
                generated_rhythm_array[beat_to_place]=1
                #When a beat is placed, set it's probability to zero
                #So we don't place it again
                rhythm_copy[start_beat] = (start_beat,0)
            else:
                print("Beat greater than 64!")

    return generated_rhythm_array

def rhythm_pattern_to_string(rhythm_array):
    """
    Taks a rhythm array and converts it into a more readable format

    Args:
        rhythm_array (list of ints): A list representing a rhythmic pattern,
        1 represents a hit and 0 represents no hit

    Returns:
        A formatted string where each 8 beat measure is seperated by a barline
    """
    #TODO
    #Account for time signatures other than 4/4
    #Add ability to skip measures or add more than one hit per measures,
    #based off of the corpus

    text = ""
    for i in range(0, len(rhythm_array)):
        if i%8==0 and i != 0:
            text+="||"
        text+=str(rhythm_array[i])

    return text


class HarmonicAnalysis:
    """
    A handy object that will take in a folder to a corpus of .hkt files,
    and provide useful stastics for the harmony, a harmonic markov model,
    and a harmonic rhythm generator.

	Args:
		songs (listof HKTObjects): A list containing HKTObjects, representing
            the corpus
        markov_model (markov_model): A model for the harmonies in the corpus
        rhythm_array (listof int): A tally array cotaining how many times a
            chord hits on the beat given the index of the beat
        prob_tuple_list (listof 2-tuples): Used to generate a weighted
            probability rhythm vector
    """
    def __init__(self, songs, state_size):
        #self.songs = tools.get_corpus_list(filepath)
        self.songs = songs
        self.markov_model = generate_markov_model(self.songs,state_size)
        self.rhythm_array = self.rhythm_analysis()
        self.prob_tuple_list = self.generate_rhythm_tuple(self.rhythm_array)

        self.chords_per_measure = self.generate_chords_per_measure()
        self.chords_per_measure_tuple = self.generate_rhythm_tuple(self.chords_per_measure)
        #print(self.chords_per_measure)

        #TODO
        #Implement
        self.chord_duration_average = 0
        self.chord_duration_stdev = 0

    def generate_progression(self):
        return self.markov_model.make_sentence()

    def get_statistics(self, filename):
        return calculate_statistics(self.songs, filename)

    #Makes a general histogram of how many chords per measure the corpus has
    #chord_array[0] = number of times chords last longer than 1 measure
    #chord_array[1] = number of times there is one chord per measure
    #chord_array[2] = number of times there is two chords per measure
    #etc
    def generate_chords_per_measure(self):
        #A tally array
        chord_array = [0]*8

        for song in self.songs:
            for segment in song.segments:
                #We need at least two chordal data points
                if len(segment.chordsNoRest) > 0:

                    last_chord_start_measure = segment.chordsNoRest[0].start_measure
                    tally = 1

                    #TODO REMOVE WHY TALLY IS DOING BAD?
                    for i in range(1, len(segment.chordsNoRest)):
                        if tally < 8:
                            #If the difference in measures between sucesssive chords is >1, that means that
                            #there is a chord longer than one measure between them
                            if int(segment.chordsNoRest[i].start_measure)-int(last_chord_start_measure) > 1:
                                chord_array[0]+=1

                            #Tally chords that have the same start measure
                            if segment.chordsNoRest[i].start_measure == last_chord_start_measure:
                                tally+=1
                            else:
                                #Increment and reset the tally once a new measure starts
                                chord_array[tally]+=1
                                tally = 1

                            last_chord_start_measure = segment.chordsNoRest[i].start_measure
                    if tally < 8:
                        chord_array[tally]+=1

        return chord_array


    def generate_rhythm_vector(self):
        pattern = generate_rhythm_pattern(self.prob_tuple_list, self.chords_per_measure_tuple)
        return rhythm_pattern_to_string(pattern)


    def rhythm_analysis(self):
        rhythm_array = [0]*8

        for song in self.songs:
            for segment in song.segments:
                for chord in segment.chordsNoRest:
                    
                    start_beat = int(((float(chord.start_beat)-1)*2))
                    #print(chord.start_beat)
                    #Make sure it doesn't break with greater than 4/4
                    if start_beat < 8:
                        rhythm_array[start_beat]+=1
                    else:
                        print("Greater than 4/4!")
            #print()

        #print(rhythm_array)
        return rhythm_array

    def generate_rhythm_tuple(self, array):
        prob_list = []

        for i in range(0,len(array)):
            prob_list.append((i,array[i]))

        return prob_list
