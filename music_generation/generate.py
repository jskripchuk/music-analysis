import os
import re

#print(os.getcwd())

#have jazz backing track
#noodle blues scale over it
#J A Z Z

text = open("music_generation/text.txt","r")

text_string = text.read()
text_arr = text_string.split()
text_sentences = re.split('[?.!]', text_string)
num_sentences = len(text_sentences)

print(len(text_sentences))

print(len(text_arr))

time_numerator = 2
