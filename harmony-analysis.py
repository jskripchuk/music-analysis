import hook

seal = hook.HKTObject("data-files/test1.hkt")

#Borred
#Returns a number that gives how many flats/sharps it is to the other mode
#EX. If we are in major and borrow from dorian mode, that's -2 (since)

#need to take care of types of sevenths


major = ["I","ii","iii","IV","V","vi","viio"]
dorian = ["i","ii","III","IV","v","vio","VII"]
phrygian = ["i","II","III","iv","vo","VI","vii"]
lydian=["I","II","iii","ivo","V","vi","vii"]
mixolydian = ["I","ii","iiio","IV","v","vi","VII"]
minor = ["i","iio","III","iv","v","VI","VII"]
locrian = ["io","II","iii","iv","V","VI","vii"]

major_int = [0,0,0,0,0,0,0]
dorian_int = [0,0,-1,0,0,0,-1]
phryg_int =[0,-1,-1,0,0,-1,-1]
lyd_int=[0,0,0,1,0,0,0]
mixo_int = [0,0,0,0,0,0,-1]
minor_int = [0,0,-1,0,0,-1,-1]
loc_int =[0,-1,-1,0,-1,-1,-1]

modes_flat_order = [locrian,phrygian,minor,dorian,mixolydian,major,lydian]
modes_scale_order = [major,dorian,phrygian,lydian,mixolydian,minor,locrian]

mode_int_flat_order = [loc_int,phryg_int,minor_int,dorian_int,mixo_int,major_int,lyd_int]
mode_int_scale_order = [major_int,dorian_int,phryg_int,lyd_int,mixo_int,minor_int,loc_int]
#modes = [major,dorian,phrygian,lydian,mixolydian,minor,locrian]


#borrow
#1 = lydian
#0= major
#-1 = mixo
#downwards in flats

maj7="maj7"
min7="min7"
min7b5="min7b5"
dom7="7"

maj9 ="maj9"
min9="min9"
#note, figure out wtf is happening with diminished chords
flat9="min7b9"
dom9="9"

seventh_qualities = [maj7,min7,min7,maj7,dom7,min7,min7b5]
ninth_qualities = [maj9,min9,flat9,maj9,dom9,min9,flat9]



#General Algorithms
#Handle borrowed chords
#Hanled Sec Chords
#Handle Normies


#Flat/Sharp
#result > 0, it's sharp
#reseult < 0, it's flat
#result = 0, no change

def handleBorrowedChord(chord):
    accidental = ""

    borrowFrom = mode_int_flat_order[int(chord.borrowed)+5]
    borrowTo = mode_int_scale_order[current_mode_num]
    sd = int(chord.scale_degree)-1
    difference = borrowFrom[sd]-borrowTo[sd]

    if difference > 0:
        accidental = "#"
    elif difference < 0:
        accidental = "b"

    roman = modes_flat_order[int(chord.borrowed)+5][sd]

    ext = getExtensionSymbol(chord,sd)
    emb = getEmbellishment(chord)

    return accidental+roman+ext+emb
    #return accidental
    #get accidental
    #get chord symbol
    #get extension
    #get embellishments
def getEmbellishment(chord):
    if chord.sus == None and chord.emb != None:
        return chord.emb
    elif chord.sus != None and chord.emb == None:
        return chord.sus
    else:
        return ""

current_mode_num = int(seal.mode)-1
current_mode = modes_scale_order[current_mode_num]

def parseChord(chord):
    sd = int(chord.scale_degree)-1

    if chord.borrowed != None:
        ###TODO FIX EXTENSIONS ON BORROWED CHORDS
        return(handleBorrowedChord(chord))
    elif chord.sec != None:
        return "secondary"
    else:
        return current_mode[sd]+getExtensionSymbol(chord,sd)+getEmbellishment(chord)

#print(current_mode_num)

def chordToRomanNumeral(chord):
    #print(chord.fb)
    #Check if it is a secondary chord
    #print(chord.sec)
    if chord.sec != None:
        extensionSymbol = "7"
        sec = "V"
        if chord.scale_degree == "4":
            sec = "IV"
        elif chord.scale_degree == "7":
            sec = "viio"
        return sec+"/"+current_mode[int(chord.sec)-1]

    #Add embellishments
    #add extensions



def getExtensionSymbol(chord,sd):
    #print(chord.fb)
    if chord.fb == "7":
        return seventh_qualities[(sd+current_mode_num)%7]
    elif chord.fb == "9":
        return ninth_qualities[(sd+current_mode_num)%7]
    elif chord.fb == "11":
        return "11"
    elif chord.fb == None:
        return ""
    else:
        return chord.fb

for segment in seal.segments:
    for chord in segment.chords:
            print(parseChord(chord))
            #print(chord.emb)

            print("-")
    print("-----")
