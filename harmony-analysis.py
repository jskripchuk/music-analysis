import hook

seal = hook.HKTObject("data-files/tennis.hkt")

#Borred
#Returns a number that gives how many flats/sharps it is to the other mode
#EX. If we are in major and borrow from dorian mode, that's -2 (since)

#need to take care of types of sevenths

major = ["I","ii","iii","IV","V","vi","viio"]
dorian = ["i","ii","III","IV","v","vio","VII"]

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

current_mode = major
current_mode_num = int(seal.mode)-1

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
        #print(chord.sec)

        return sec+"/"+current_mode[int(chord.sec)-1]

    #Add embellishments
    #add extensions

def getExtensionSymbol(chord):
    sd = int(chord.scale_degree)-1
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
        print(chordToRomanNumeral(chord))
        #chord_info = chord.sec
        #print(chord_info)
        #print(chord.scale_degree)
        #print(determineExtensionSymbol(chord))
        #print(chordToRomanNumeral(chord))
        print("-")
    print("-----")
