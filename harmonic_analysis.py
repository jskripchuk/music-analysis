import hkt_generator
import statistics
import markovify
import graphing
from random import random
from bisect import bisect
from os import listdir

"""
harmonic_analysis.py

Takes the Hooktheory corpus of an artist and performs a statistical analysis,
of the harmony. Also creates a markov model that can generate a harmonic
progression and rhythm.

"""

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

def calculate_statistics(songs):
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

    getExtensions = lambda chord: chord.extension_disc

    getSus = lambda chord: chord.sus
    getEmb = lambda chord: chord.emb

    #Create histograms
    full_chord_frequency = createHistogram(songs,getChordsNoRest,getRoman)
    basic_chord_frequency = createHistogram(songs,getChordsNoRest,getRomanBasic)
    extension_frequency = createHistogram(songs,getChordsNoRest,getExtensions)

    #Merge sus and emb chords into one graph
    sus_frequency = createHistogram(songs,getChordsNoRest,getSus)
    emb_frequency = createHistogram(songs,getChordsNoRest,getEmb)

    total_emb_frequency = emb_frequency.copy()
    total_emb_frequency.update(sus_frequency)

    #Generate graphs
    plotBarChartFromDict(basic_chord_frequency,"Basic Chord Types","basic_roman_numerals")
    plotBarChartFromDict(full_chord_frequency,"Chord Types with Extensions","full_roman_numerals")
    plotBarChartFromDict(total_emb_frequency,"Embellishments","embellishments")
    plotBarChartFromDict(extension_frequency,"Just Extensions","extensions")


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
            for chord in segment.chordsNoRest:
                text+=chord.roman_basic+" "

        #We create a seperate model for every song and put them into a list
        model = markovify.Text(text,state_size=model_state_size)
        markovs.append(model)

    #Then we combine all the models in the list
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
        chords_this_measure = weighted_choice(chords_per_measure)

        #Generate how ever many chords we have to
        for j in range(0, chords_this_measure):
            #Figure out what beat to place them on
            start_beat = weighted_choice(rhythm_copy)
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

def get_corpus_list(folder):
    """
    Generates a rhythm pattern based of the "hit-vector" given.

    Args:
        rhythm_prob (list of ints [size=8]): A list where each index contains
            how many times a chord started on that index.

    Returns:
        An array that contains a rhythmic pattern, where 0 is no hit and 1 is
        a hit. This array represents one segment of a song.
    """
    songs = []

    for filename in listdir(folder):
        path = folder+"/"+filename
        new_song = hkt_generator.HKTObject(path)
        songs.append(new_song)

    return songs


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
    def __init__(self, filepath, state_size):
        self.songs = get_corpus_list(filepath)
        self.markov_model = generate_markov_model(self.songs,state_size)
        self.rhythm_array = self.rhythm_analysis()
        self.prob_tuple_list = self.generate_rhythm_tuple(self.rhythm_array)

        self.chords_per_measure = self.generate_chords_per_measure()
        self.chords_per_measure_tuple = self.generate_rhythm_tuple(self.chords_per_measure)

        #TODO
        #Implement
        self.chord_duration_average = 0
        self.chord_duration_stdev = 0

    def generate_progression(self):
        return self.markov_model.make_sentence()

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

                    for i in range(1, len(segment.chordsNoRest)):
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

                    #Make sure it doesn't break with greater than 4/4
                    if start_beat < 8:
                        rhythm_array[start_beat]+=1
                    else:
                        print("Greater than 4/4!")

        return rhythm_array

    def generate_rhythm_tuple(self, array):
        prob_list = []

        for i in range(0,len(array)):
            prob_list.append((i,array[i]))

        return prob_list
