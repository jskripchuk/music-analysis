import json_chord_to_roman
import json
import codecs

from xml.dom.minidom import parse
import xml.dom.minidom


class Note:
	"""
	Note represents the XML representation of a hooktheory note

	Args:
		start_beat_abs (str):
		start_measure (str):
		note_length (str):
		scale_degree (str):
		octave (str):
		isRest (str):
	"""
	def __init__(self, start_beat_abs, start_measure, note_length,
				scale_degree, octave, isRest):
		self.start_beat_abs = start_beat_abs
		self.start_measure = start_measure
		self.note_length = note_length
		self.scale_degree= scale_degree
		self.octave = octave
		self.isRest = isRest

class Chord:
	"""
	Chord represents the XML representation of a hooktheory chord

	Args:
		scale_degree (str):
		fb (str):
		sec (str):
		sus (str):
		pedal (str):
		alternate (str):
		borrwed (str):
		chord_duration (str):
		start_measure (str):
		start_beat (str):
		start_beat_abs (str):
		isRest (str):
		emb (str):
		roman (str):
		roman_basic (str):
		extension_disc (str):
		accidental(str):
	"""

	def __init__(self, scale_degree, fb, sec, sus, pedal, alternate,
				borrowed, chord_duration, start_measure, start_beat,
				start_beat_abs, isRest,emb, adds):
		self.scale_degree = scale_degree
		self.fb = fb
		self.sec = sec
		self.sus = sus
		self.pedal = pedal
		self.alternate = alternate
		self.borrowed = borrowed
		self.chord_duration = chord_duration
		self.start_measure = start_measure
		self.start_beat = start_beat
		self.start_beat_abs = start_beat_abs
		self.isRest = isRest
		self.emb = emb
		self.roman = ""
		self.roman_basic = ""
		self.extension_disc = ""
		self.accidental = ""
		self.adds = adds

def createChord(chordDom):
	scale_degree = getData(chordDom, "sd")
	fb = getData(chordDom, "fb")
	sec = getData(chordDom, "sec")
	sus = getData(chordDom, "sus")
	pedal = getData(chordDom, "pedal")
	alternate = getData(chordDom, "alternate")
	borrowed = getData(chordDom, "borrowed")
	chord_duration = getData(chordDom, "chord_duration")
	start_measure = getData(chordDom, "start_measure")
	start_beat = getData(chordDom, "start_beat")
	start_beat_abs = getData(chordDom, "start_beat_abs")
	isRest = getData(chordDom, "isRest")
	emb = getData(chordDom,"emb")

	chord = Chord(scale_degree, fb, sec, sus, pedal, alternate, borrowed,
		chord_duration, start_measure, start_beat, start_beat_abs, isRest,emb)

	return chord

##IMPLEMENT
#FINIHSL ATER
def createChordJSON(chordJSON):
	scale_degree = chordJSON["root"]
	fb = chordJSON["inversion"]
	sus = chordJSON["suspensions"]
	sec = chordJSON["applied"]
	pedal = chordJSON["pedal"]
	alternate = chordJSON["alterations"]
	borrowed = chordJSON["borrowed"]
	chord_duration = chordJSON["duration"]
	start_measure = ((chordJSON["beat"]-1)//4)+1
	start_beat = (chordJSON["beat"]-1)%4
	start_beat_abs = chordJSON["beat"]
	isRest = chordJSON["isRest"]
	emb = chordJSON["type"]
	adds = chordJSON["adds"]

	chord = Chord(scale_degree, fb, sec, sus, pedal, alternate, borrowed,
		chord_duration, start_measure, start_beat, start_beat_abs, isRest,emb, adds)

	return chord

class Segment:
	def __init__(self):
		self.melody = []
		self.chords = []
		self.melodyNoRest = []
		self.chordsNoRest = []

	def addNote(self,note):
		self.melody.append(note)

	def addNoteNoRest(self,note):
		if note.isRest == "0" or note.isRest == False:
			self.melodyNoRest.append(note)

	def addChord(self, chord):
		self.chords.append(chord)

	def addChordNoRest(self,chord):
		self.chordsNoRest.append(chord)

	def printNotes(self):
		for i in self.melody:
			print(i.scale_degree)

	def printChords(self):
		for i in self.chords:
			print(i.scale_degree)

#mode
#1=major
#2 = dorian
#3 = prygian
class HKTObject:
	def __init__(self, filepath):

		JSON = True
		self.segments = []


		if JSON:
			song = json.load(codecs.open(filepath,'r','utf-8-sig'))
			#print(song)
			self.artist = None
			self.title = filepath
			self.bpm = song["tempos"][0]["bpm"]
			self.key = song["keys"][0]["tonic"]
			self.mode = song["keys"][0]["scale"]
			self.youtubeID = song["youtube"]["id"]

			

			self.segments.append(createSegmentJSON(song))

			for segment in self.segments:
				for chord in segment.chords:
					chord.roman = json_chord_to_roman.parseChord(chord, self.mode)
					segment.addChordNoRest(chord)
					#print(chord.roman)

		else:
			DOMTree = xml.dom.minidom.parse(filepath)
			collection = DOMTree.documentElement

			self.artist = getData(collection, "artist")
			self.title = getData(collection, "title")
			self.bpm = getData(collection, "BPM")
			self.key = getData(collection, "key")
			self.mode = getData(collection, "mode")
			self.youtubeID = getData(collection, "YouTubeID")

			for segment in DOMTree.getElementsByTagName("segment"):
				self.segments.append(createSegment(segment))

		
		#print(self.title)
		#for segment in self.segments:
		#	for chord in segment.chords:
		#		chord.extension_disc = ""
		#		if chord.isRest == "0":
		#			chord.roman = chord_to_roman.parseChord(chord,self.mode)
		#			segment.addChordNoRest(chord)
		#		else:
		#			chord.roman = "REST"


def createSegment(segmentDom):
	segment = Segment()
	for note in segmentDom.getElementsByTagName("note"):
		segment.addNote(createNote(note))
		segment.addNoteNoRest(createNote(note))

	for chord in segmentDom.getElementsByTagName("chord"):
		segment.addChord(createChord(chord))

	return segment

##IMPLEMENT
def createSegmentJSON(segmentJSON):
	segment = Segment()
	for note in segmentJSON["notes"]:
		segment.addNote(createNoteJSON(note))
		segment.addNoteNoRest(createNoteJSON(note))

	for chord in segmentJSON["chords"]:
		segment.addChord(createChordJSON(chord))
		#segment.addChordNoRest(createChordJSON(chord))

	return segment

def createNote(noteDom):
	start_beat_abs = getData(noteDom, "start_beat_abs")
	start_measure = getData(noteDom, "start_measure")
	note_length = getData(noteDom, "note_length")
	scale_degree = getData(noteDom, "scale_degree")
	octave = getData(noteDom, "octave")
	isRest = getData(noteDom, "isRest")

	note = Note(start_beat_abs, start_measure, note_length,
			scale_degree, octave, isRest)

	return note

##IMPLEMENT

#Assuming 4 beats per bar
def createNoteJSON(noteJSON):
	start_beat_abs = noteJSON["beat"]

	#Assume 4 beats per measure
	start_measure = ((noteJSON["beat"]-1)//4)+1
	note_length = noteJSON["duration"]
	scale_degree = noteJSON["sd"]
	octave = noteJSON["octave"]
	isRest = noteJSON["isRest"]

	note = Note(start_beat_abs, start_measure, note_length,
			scale_degree, octave, isRest)

	return note



def getData(dom, tag):
	if len(dom.getElementsByTagName(tag)) == 0:
		return None

	if len(dom.getElementsByTagName(tag)[0].childNodes) == 0:
		return None
	else:
		return dom.getElementsByTagName(tag)[0].childNodes[0].data
