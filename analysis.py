import music21

clarity = music21.converter.parse('clarity.mxl')
##sBach.show()

melody = clarity.parts[0]
harmony = clarity.parts[1]

#clarity.show()

stack = clarity.measure(1)
#stack.show()

#chordify.show()

stack = stack.stripTies()
#stack.show()
flat = stack.flat
#stack.show()



print("Note start times")
for i in flat.getElementsByClass("Note"):
    print(i.offset)

print("")

#if the start of a melody note falls within the duration range, then count it as
#part of the chord
#eg. start <= node < end (non inclusive)
print("   ")

for i in flat.getElementsByClass("Chord"):
    print(i.offset)
    print(i.duration.quarterLength)
    print("----")

#stack.show()

#for i in harmony.recurse():
    #print(i)

#print(notes[1].activeSite)
