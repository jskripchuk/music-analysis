import hook

seal = hook.HKTObject("data-files/seal.hkt")

melody = seal.segments[0].melody



def getScaleDegreeHistogram(melody): #Only diatonic currently
	histogram = [0,0,0,0,0,0,0]
	
	for note in melody:
		sd = note.scale_degree
		#print(sd + ":" +note.octave)
		try:
			sd = int(sd)
			histogram[sd-1]+=1
		except:
			False

	return histogram

def getIntervalHistogram(melody): #Only diatonic currently
	#goes up to 12th
	#DOES NOT ACCOUNT FOR RESTS: FIX SOON
	histogram = [0,0,0,0,0,0,0,0,0,0,0,0]

	for i in range(0,len(melody)-1):
		note1 = melody[i]
		note2 = melody[i+1]
		
		try:
			note1Val = getAbsoluteScaleDegree(note1)

			note2Val =getAbsoluteScaleDegree(note2)

			diff = abs(note2Val-note1Val)
			histogram[diff]+=1
		except:
			False
	return histogram


import statistics
def calculateContourAndRange(melody):
	contourChanges = 0
	melodyRange = 0
	
	minNote = 0
	maxNote = 0

	increasing = True

	notesPerCSeg = []
	currentNotesPerCSeg = 0


	for i in range(0,len(melody)-1):
		note1 = melody[i]
		note2 = melody[i+1]
		try:
			absolute1 = getAbsoluteScaleDegree(note1)
			absolute2 = getAbsoluteScaleDegree(note2)
			minNote = min(absolute1,minNote)
			maxNote = max(absolute1,maxNote)

			diff = absolute2-absolute1
			
			currentNotesPerCSeg += 1
			

			if diff > 0 and not increasing:
				contourChanges += 1
				increasing = not increasing
				notesPerCSeg.append(currentNotesPerCSeg)
				currentNotesPerCSeg = 0
			elif diff < 0 and increasing:
				contourChanges += 1
				increasing = not increasing
				notesPerCSeg.append(currentNotesPerCSeg)
				currentNotesPerCSeg = 0
			
		except:
			False
	
	##close enough i guess
	melodyRange = maxNote-minNote
	print("Range: "+str(melodyRange))
	print("Num Contour Changes: "+str(contourChanges))
	print("Notes per CSeg:" +str(notesPerCSeg))
	
	cursum = 0
	for i in notesPerCSeg:
		cursum+=i
	avgCseg = cursum/len(notesPerCSeg)
	print("Average notes per Cseg: "+str(avgCseg))	
	print("StDv Cseg: "+str(statistics.stdev(notesPerCSeg)))



def getAbsoluteScaleDegree(note):
	return int(note.scale_degree)+int(note.octave)*7

def probDistFromHistogram(hist):
	totalSum = 0
	
	histCopy = list(hist)	
	
	for i in hist:
		totalSum+=i

	for i in range(0, len(hist)):
		histCopy[i] = histCopy[i]/totalSum

	return histCopy
		

sdHist = getScaleDegreeHistogram(melody)
intervalHist = getIntervalHistogram(melody)

print()
print("Melody Data")
print("====================")
print("Scale Degrees: "+str(sdHist))
print("Scale Degree Prob: "+str(probDistFromHistogram(sdHist)))
print()
print("Intervals: "+str(intervalHist))
print("Intervals Prob: "+str(probDistFromHistogram(intervalHist)))
print()
calculateContourAndRange(melody)
