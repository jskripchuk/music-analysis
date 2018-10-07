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
    chord_type = ""
    
    if chord.type != 5:

    
    print(result)

    return ""

def getAccidental(chord, mode):
    return ""

def parseChord(chord, mode):
    
    if chord.borrowed != "":
        handleBorrowed(chord, mode)
