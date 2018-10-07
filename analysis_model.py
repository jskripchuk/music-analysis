import melodic_analysis
import harmonic_analysis
import tools

class CorpusAnalysis:
    def __init__(self, filepath, gesture_rest):
        self.songs = tools.get_corpus_list(filepath)
        #self.melody_model = melodic_analysis.MelodicAnalysis(self.songs,1,gesture_rest)
        #self.harmonic_model = harmonic_analysis.HarmonicAnalysis(self.songs,1)

    def print_songs(self):
        for song in self.songs:
            print(song.title)
            for segment in song.segments:
                print("##########")
                for chord in segment.chords:
                    print(chord.roman)
					#chord.roman = json_chord_to_roman.parseChord(chord, self.mode)
					#segment.addChordNoRest(chord)
                print("###########")

    def generate_progression(self):
        return self.harmonic_model.markov_model.make_sentence()

    def generate_melodic_sequence(self):
        return self.melody_model.markov_model.make_sentence()

    def get_gestures_in_corpus(self):
        return self.melody_model.get_gestures_in_corpus()
    
    def generate_harmonic_rhythm(self):
        return self.harmonic_model.generate_rhythm_vector()

    def calculate_statistics(self):
        return self.harmonic_model.get_statistics()

    def get_solfege_histogram(self):
        self.melody_model.get_histogram()
