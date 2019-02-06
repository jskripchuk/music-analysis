"""
json_chord_to_roman.py

Used to conver the HKT_Object representation of a chord,
and convert it to a roman numeral. This is specifically for a JSON representation.

"""

import functools

#The chord functions of the basic diatonic modes
major = ["I","ii","iii","IV","V","vi","viio"]
dorian = ["i","ii","III","IV","v","vio","VII"]
phrygian = ["i","II","III","iv","vo","VI","vii"]
lydian=["I","II","iii","ivo","V","vi","vii"]
mixolydian = ["I","ii","iiio","IV","v","vi","VII"]
minor = ["i","iio","III","iv","v","VI","VII"]
locrian = ["io","II","iii","iv","V","VI","vii"]

#Integer representation on what scale degrees are flat/sharp compared to a
#zero vector representing major
major_int = [0,0,0,0,0,0,0]
dorian_int = [0,0,-1,0,0,0,-1]
phryg_int =[0,-1,-1,0,0,-1,-1]
lyd_int=[0,0,0,1,0,0,0]
mixo_int = [0,0,0,0,0,0,-1]
minor_int = [0,0,-1,0,0,-1,-1]
loc_int =[0,-1,-1,0,-1,-1,-1]

mode_dic_to_flats = {"major": major_int, "dorian": dorian_int, "phyrigan": phryg_int, "lydian": lyd_int, "mixolydian": mixo_int, "minor": minor_int, "locrian": loc_int}
mode_dic_to_roman = {"major": major, "dorian": dorian, "phyrgian": phrygian, "lydian": lydian, "mixolydian": mixolydian, "minor": minor, "locrian": locrian}
mode_offsets = {"major": 0, "dorian": 1, "phyrgian": 2, "lydian": 3, "mixolydian": 4, "minor": 5, "locrian":6}

#Extension qualities that are not represented in HKT files
#Sevenths
maj7="maj7"
min7="min7"
min7b5="min7b5"
dom7="7"

#Ninths
maj9 ="maj9"
min9="min9"
flat9="min7b9"
dom9="9"

#Eleventh
eleventh = "11"

#Thirteenth
thirteen = "13"

#The seventh and ninth qualities of the major diatonic scale
#Can be used modally by offsett+modular arithmitic
seventh_qualities = [maj7,min7,min7,maj7,dom7,min7,min7b5]
ninth_qualities = [maj9,min9,flat9,maj9,dom9,min9,flat9]

def handleBorrowed(chord, mode):
    sd = chord.scale_degree
    #print(sd)

    #Want to find out if we should sharp or flat this roman numeral (if it's borrowed)
    #Does this using the "flat" representaion of a scale
    
    #Best explained via examples:

    #Borrowing the #ivo chord from lydian in major
    #lydian[3] = 1 (4-1=3 because arrays start at 0)
    #major[3] = 0
    #1-0 = 1 > 0 : So thus we sharpen it

    #Borrowing the bIII from minor in lydian
    #minor[2]= -1
    #lydian[2] = 0
    #-1 - 0 = -1 < 0: so thus we flat it

    #Borrowing the ii from minor in lydian (we don't sharp or flat in this case)
    #minor[1] = 0
    #lydian[1] = 0
    #0-0 = 0 : so thus we do nothing
    diff = mode_dic_to_flats[chord.borrowed][sd-1]-mode_dic_to_flats[mode][sd-1]

    accidental = ""
    if diff > 0:
        accidental="#"
    elif diff < 0:
        accidental="b"

    roman = accidental+mode_dic_to_roman[chord.borrowed][sd-1]
    chord.roman_basic = roman
    chord_type = getChordType(chord, chord.borrowed)


    return roman+chord_type+getEmbellishments(chord)
    
def getChordType(chord, mode):
    sd = chord.scale_degree
    arr_loc = (mode_offsets[mode]+(sd-1))%len(seventh_qualities)
    if chord.emb == 11:
        return eleventh
    elif chord.emb == 13:
        return thirteen
    elif chord.emb == 7:
        return seventh_qualities[arr_loc]
    elif chord.emb == 9:
        return ninth_qualities[arr_loc]
    else:
        return ""

def getAlterations(chord):
    result = ""
    for i in chord.alternate:
        result+=i

    return result

def getSuspensions(chord):
    result = ""

    for i in chord.sus:
        result+="sus"+str(i)
    
    return result

def getAdds(chord):
    result = ""

    for i in chord.adds:
        result+="add"+str(i)
    
    return result

def getEmbellishments(chord):
    suspensions = getSuspensions(chord)
    alterations = getAlterations(chord)
    adds = getAdds(chord)

    return suspensions+alterations+adds

def handleApplied(chord,mode):
    roman = ""

    if chord.sec == 5:
        roman = "V"
    elif chord.sec == 4:
        roman = "IV"
    elif chord.sec == 7:
        roman = "viio"

    if chord.emb == 11:
        roman+="11"
    elif chord.emb == 13:
        roman+="13"
    elif chord.emb == 7:
        roman+= seventh_qualities[chord.sec-1]
    elif chord.emb == 9:
        roman+= ninth_qualities[chord.sec-1]

    roman_basic = roman

    roman+=getEmbellishments(chord)

    roman_basic+="/"+mode_dic_to_roman[mode][chord.scale_degree-1]
    chord.roman_basic = roman_basic

    roman+="/"+mode_dic_to_roman[mode][chord.scale_degree-1]

    return roman



def parseChord(chord, mode):
    try:
        roman = ""
        if chord.borrowed != "" and chord.borrowed != None:
            roman = handleBorrowed(chord, mode)
        elif chord.sec != 0:
            roman = handleApplied(chord,mode)
        else:
            roman = mode_dic_to_roman[mode][chord.scale_degree-1]
            chord.roman_basic = roman
            roman+=getChordType(chord,mode)
            roman+=getEmbellishments(chord)

        chord.roman = roman
        return roman
    except:
        chord.roman = ""
        print("skipping chord..")
        return ""

    #suspensions = getSuspensions(chord)
    #alterations = getAlterations(chord)

    #full_roman = roman+suspensions+alterations

    

    #print(roman)
    #return roman
    