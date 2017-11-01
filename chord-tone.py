import music21
from music21 import roman

clarity = music21.converter.parse('data-files/clarity.mxl')
##sBach.show()


mode = "major"
key = clarity.flat.getElementsByClass("KeySignature")[0].asKey(mode)



melody = clarity.parts[0]
harmony = clarity.parts[1]

stack = clarity

stack = stack.stripTies()
flat = stack.flat

notes = []


for i in melody.stripTies().flat.getElementsByClass("Note"):
	notes.append(i)
	#print(i)

chords = []

#for i in harmony.stripTies().flat.getElementsByClass("Note"):
	#print(i.lyric)
	#numeral = roman.RomanNumeral(i.lyric)
	#numeral.key = key
	#numeral.writeAsChord=True
	#numeral.offset = i.offset
	#numeral.duration = i.duration
	#print(numeral.pitches)
	#chords.append(numeral)
	#print(roman.RomanNumeral("V").writeAsChord=True)





for i in flat.getElementsByClass("Chord"):
	#print(i)
	i.melodyChordTones = []
	i.melodyIntervals = []
	i.melodyIntervalsSimple = []
	chords.append(i)
	



#if the start of a melody note falls within the duration range, then count it as
#part of the chord
#eg. start <= node < end (non inclusive)

#Melody Intervals is the interval between the root of the chord and the melody note
#Compressed within an octave, so 2nds=9th, 4ths=11th 6ths can be 13ths too

#Can also just have students put the roman numeral name?
def fillChordTonesHard(chords):
	noteIndex = 0
	for chord in chords:
		while noteIndex < len(notes):
			currentNote = notes[noteIndex]
			chordEnd = chord.duration.quarterLength+chord.offset


			if currentNote.offset >= chord.offset and currentNote.offset < chordEnd:
				chord.melodyChordTones.append(currentNote)
				interval = music21.interval.Interval(chord.root(),currentNote.pitch)
				chord.melodyIntervals.append(interval)
				chord.melodyIntervalsSimple.append(interval.simpleName)
				noteIndex+=1
			else:
				break

fillChordTonesHard(chords)

for chord in chords:
	print("====================================")
	print(chord)
	#print(chord.commonName)
	#print(chord.melodyChordTones)
	print(chord.melodyIntervalsSimple)
	#print(chord.melodyIntervals)
	#print(chord.melodyChordTones)
	print("====================================")
	print()
	

#Now have chords and their melody chord tones
#If two chords have the same closed position

		
		
