import os
import re
import music21
import random
import os
from textblob import TextBlob

script_dir = os.path.dirname(__file__)
text = open(os.path.join(script_dir,"text.txt"))

#text = open("text.txt","r")

text_string = text.read()
text_arr = text_string.split()
text_sentences = re.split('[?.!]', text_string)
num_sentences = len(text_sentences)

#interval vectors of different scales
pentatonic = [0,2,4,7,9]

diatonic_major = [0,2,4,5,7,9,11]
diatonic_minor = [0,2,3,5,7,8,10]

twelve_tone = [0,1,2,3,4,5,6,7,8,9,10,11]

rhythms = [4,2,1,.5,0.25]

#print(len(text_sentences))

#print(len(text_arr))

f = music21.note.Note("F5")
s = music21.stream.Stream()

numerator = len(text_arr)%2+3
denom = 4

meter = music21.meter.TimeSignature(str(numerator)+"/"+str(denom))
tempo = music21.tempo.MetronomeMark(number=200)
s.append(tempo)
s.append(meter)


root = 48

major_vec = diatonic_major
minor_vec = diatonic_minor
current_interval_vector = diatonic_minor

prev = root+current_interval_vector[random.randint(0, len(current_interval_vector)-1)]

sd = 7

prev = root

array_size = 10
sentiment_average = 0
running_array = [0]*array_size

def calculateAverageSentiment():
    sum = 0
    for num in running_array:
        sum+=num
    return sum/array_size

current_sentiment_spot = 0

for string in text_arr:
    word_stat = TextBlob(string)
    running_array[current_sentiment_spot] = TextBlob(string).sentiment.polarity
    current_sentiment_spot = (current_sentiment_spot+1)%array_size
    average_sent = calculateAverageSentiment()

    if average_sent >= 0:
        current_interval_vector = major_vec
    else:
        current_interval_vector = minor_vec
    #print()

    #print(str(word_stat.sentiment.polarity)+","+str(calculateAverageSentiment()))
    note = (ord(string[0]))%len(current_interval_vector)-1
    rhythm = rhythms[ord(string[-1])%len(rhythms)]
    sd = current_interval_vector[note]

    if abs((root+sd)-prev) < abs((root-12+sd)-prev):
        prev = root+sd
    else:
        prev = root-12+sd

    append_note = music21.note.Note(prev)
    append_note.quarterLength = rhythm
    append_note.lyric = string
    s.append(append_note)

time_numerator = 2


s.show()
