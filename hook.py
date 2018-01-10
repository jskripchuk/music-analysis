import chord_to_roman

from xml.dom.minidom import parse
import xml.dom.minidom


class Note:
	def __init__(self, start_beat_abs, start_measure, note_length,
				scale_degree, octave, isRest):
		self.start_beat_abs = start_beat_abs
		self.start_measure = start_measure
		self.note_length = note_length
		self.scale_degree= scale_degree
		self.octave = octave
		self.isRest = isRest

class Chord:
	def __init__(self, scale_degree, fb, sec, sus, pedal, alternate, borrowed,
			chord_duration, start_measure, start_beat, start_beat_abs, isRest,emb):
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

class Segment:
	def __init__(self):
		self.melody = []
		self.chords = []

	def addNote(self,note):
		self.melody.append(note)

	def addChord(self, chord):
		self.chords.append(chord)

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

		DOMTree = xml.dom.minidom.parse(filepath)
		collection = DOMTree.documentElement

		self.segments = []
		self.artist = getData(collection, "artist")
		self.title = getData(collection, "title")
		self.bpm = getData(collection, "BPM")
		self.key = getData(collection, "key")
		self.mode = getData(collection, "mode")
		self.youtubeID = getData(collection, "YouTubeID")

		for segment in DOMTree.getElementsByTagName("segment"):
			self.segments.append(createSegment(segment))

		for segment in self.segments:
			for chord in segment.chords:
				#Oh I feel super bad for tacking on extension quality but it's gotta be done
				chord.extension_disc = ""
				chord.roman = chord_to_roman.parseChord(chord,self.mode)

def createSegment(segmentDom):
	segment = Segment()
	for note in segmentDom.getElementsByTagName("note"):
		segment.addNote(createNote(note))

	for chord in segmentDom.getElementsByTagName("chord"):
		segment.addChord(createChord(chord))

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


def getData(dom, tag):
	if len(dom.getElementsByTagName(tag)) == 0:
		return None

	if len(dom.getElementsByTagName(tag)[0].childNodes) == 0:
		return None
	else:
		return dom.getElementsByTagName(tag)[0].childNodes[0].data
