#TODO: Remove o from diminished chords when adding extension
#Not really pressing

"""
chord_to_roman.py

Used to conver the HKT_Object representation of a chord,
and convert it to a roman numeral.

"""

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

#Hooktheory uses a "flat order" representation for a borrwed Chord
#However uses a "scale order" when represeting the mode of a whole Song
#Let it be known, it was quite a pain to deal with.

#FLAT ORDER
#If the major scale has 0 flats, each mode is represnted by how many flats it is
#away from major. (Lydian being the only positive since it is one sharp)
#----------
#Lydian = 1
#Major/Ionian = 0
#Mixolydian = -1
#Dorian = -2
#Minor/Aeolian = -3
#Phrygian = -4
#Locrian = -5

#SCALE ORDER
#Using 1 as major, and incrementing the mode based off of the next scale degree
#----------
#Major/Ionian = 1
#Dorian = 2
#Phrygian = 3
#Lydian = 4
#Mixolydian = 5
#Minor/Aeolian = 6
#Locrian = 7

modes_flat_order = [locrian,phrygian,minor,dorian,mixolydian,major,lydian]
modes_scale_order = [major,dorian,phrygian,lydian,mixolydian,minor,locrian]

mode_scale_dict = {"major": 1, "dorian": 2, "phrygian": 3, "lydian": 4, "mixolydian": 5, "minor": 6, "locrian": 7}
mode_flat_order = {"locrian": 0, "phrygian": 1, "minor": 2, "dorian": 3, "mixolydian": 4, "major": 5, "lydian": 6}

mode_int_flat_order = [loc_int,phryg_int,minor_int,
                        dorian_int,mixo_int,major_int,lyd_int]
mode_int_scale_order = [major_int,dorian_int,phryg_int,
                        lyd_int,mixo_int,minor_int,loc_int]

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

#The seventh and ninth qualities of the major diatonic scale
#Can be used modally by offsett+modular arithmitic
seventh_qualities = [maj7,min7,min7,maj7,dom7,min7,min7b5]
ninth_qualities = [maj9,min9,flat9,maj9,dom9,min9,flat9]


def handleBorrowedChord(chord,current_mode,current_mode_num):
    """
    Takes in a HKT borrwed chord, and then converts it to it's correct roman
    numeral notation.

    Args:
        chord: An HKT chord object.
        current_mode: An array with diatonic chord strings of the current mode.
        current_mode_num: The Hooktheory number representation of the mode.

    Returns:
        The roman numeral notation of the borrowed chord, respect to the
        current mode.
    """

    accidental = ""

    #In order to make sure we have the correct accidental we must figure out
    #if the borrowed chord is sharp or flat. (It is possible to borrow, yet
    #have no accidental eg. in major borrowing a dorian IV7)

    #Takes our integer representation of the modes, and subtracts the
    #two integers at the correct scale degree to get either 1,-1, or 0

    #We add +5 to chord.borrowed since it is in the range [-5,1]
    #We need [0,6] for our array
    #print(chord.borrowed)
    if(int(chord.borrowed)+5 < len(mode_int_flat_order)):
        borrowFrom = mode_int_flat_order[int(chord.borrowed)+5]
        borrowTo = mode_int_scale_order[current_mode_num]
        sd = int(chord.scale_degree)-1
        difference = borrowFrom[sd]-borrowTo[sd]

    #If the difference is positive, we need to sharpen the note
    #If the difference is negative, we need to flatten it
    #Else we have no accidental
        if difference > 0:
            accidental = "#"
        elif difference < 0:
            accidental = "b"

    #Our base roman numeral is the chord from the mode we borrow from
        roman = modes_flat_order[int(chord.borrowed)+5][sd]

    #A quick and dirty index map from the scale order to the flat order array
    #Used to alculate the correct quality of the chord extension
        swap = [6,2,5,1,4,0,3]
        borrowNum = swap[int(chord.borrowed)+5]
        index = (borrowNum+sd)%7

        ext = getExtensionSymbol(chord,index)
        emb = getEmbellishment(chord)

        chord.extension_disc = ext
        chord.roman_basic = accidental+roman
        chord.accidental = accidental

        return accidental+roman+ext+emb
    else:
        #Hooktheory breaks when you go up the circle fifths
        #TODO: Fix this, but I will never fix this
        #print("BAD CHORD")
        return ""

def getEmbellishment(chord):
    """
    Returns the embellishment of the given chord.
    Even though in Hooktheory add9 counts as an embellishment, it is represented
    as a suspension chord for some reason. But in all cases a chord having an
    embellishment and a suspension is disjoint.

    Args:
        chord: An HKT chord object.

    Returns:
        The embellishment of the given chord if there is one. An empty string
        if there is not.
    """

    print(chord.adds)
    if chord.adds != []:
        return "add"+"".join(map(str,chord.adds))
    else:
        return ""

def handleSecondaryChord(chord,current_mode,current_mode_num):
    """
    Takes a HKT secondary chord and parses it into roman numeral notation

    Args:
        chord: An HKT chord object.
        current_mode: An array with diatonic chord strings of the current mode.
        current_mode_num: The Hooktheory number representation of the mode.

    Returns:
        The secondary HKT chord in roman numeral notation.
    """

    extensionSymbol = ""
    sec = ""

    if chord.scale_degree == "5":
        sec = "V"
    elif chord.scale_degree == "4":
        sec = "IV"
    elif chord.scale_degree == "7":
        sec = "viio"


    #Extension types are fixed, so no need to look into the qualties arr
    if chord.fb == "7":
        if chord.scale_degree == "5":
            extensionSymbol = dom7
        elif chord.scale_degree == "4":
            extensionSymbol = maj7
        elif chord.scale_degree == "7":
            extensionSymbol = min7b5
    elif chord.fb == "9":
        if chord.scale_degree == "5":
            extensionSymbol = dom9
        elif chord.scale_degree == "4":
            extensionSymbol = maj9
        elif chord.scale_degree == "7":
            extensionSymbol = min7b9
    elif chord.fb == "11":
            extensionSymbol = eleventh
    elif chord.fb == None:
            extensionSymbol = ""
    else:
            extensionSymbol = chord.fb

    chord.extension_disc = extensionSymbol
    chord.roman_basic = sec+"/"+current_mode[int(chord.sec)-1]
    emb = getEmbellishment(chord)

    return sec+extensionSymbol+emb+"/"+current_mode[int(chord.sec)-1]

def getExtensionSymbol(chord,index):
    """
    Takes a HKT secondary chord and parses it into roman numeral notation

    Args:
        chord: An HKT chord object.
        current_mode: An array with diatonic chord strings of the current mode.
        current_mode_num: The Hooktheory number representation of the mode.

    Returns:
        The secondary HKT chord in roman numeral notation.
    """

    if chord.fb == "7":
        return seventh_qualities[index]
    elif chord.fb == "9":
        return ninth_qualities[index]
    elif chord.fb == "11":
        return eleventh
    elif chord.fb == None:
        return ""
    else:
        return chord.fb



def parseChord(chord, modeNum):
    """
    Takes in any type of HKT chord, and decides how to parse it into roman
    numeral notation.
    The three cases are:
        -Strict Diatonic ("Normal")
        -Borrwed Chord
        -Secondary Chord

    Args:
        chord: An HKT chord object.
        modeNum: The HKT numerical representation of the song's mode

    Returns:
        The HKT chord in roman numeral notation.
    """

    #Offset by 1 to start at 0
    sd = int(chord.scale_degree)-1

    #print(modeNum)
    modeNum = mode_scale_dict[modeNum]
    current_mode_num = int(modeNum)-1
    current_mode = modes_scale_order[current_mode_num]

    if chord.borrowed != None:
        return handleBorrowedChord(chord,current_mode,current_mode_num)
    elif chord.sec != 0:
        return handleSecondaryChord(chord,current_mode,current_mode_num)
    else:
        index = (sd+current_mode_num)%7
        print(current_mode_num)
        #chord.extension_disc = getExtensionSymbol(chord,index)
        chord.extension_dict = ""
        chord.roman_basic = current_mode[sd]
        #print(chord.adds)
        return current_mode[sd]+chord.extension_disc+getEmbellishment(chord)
