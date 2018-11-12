import melodic_analysis
import harmonic_analysis
import tools
import plotly.plotly
import plotly.graph_objs as go
import statistics 



class CorpusAnalysis:
    def __init__(self, filepath):
        self.songs = tools.get_corpus_list(filepath)
        self.melody_model = melodic_analysis.MelodicAnalysis(self.songs,1)
        self.harmonic_model = harmonic_analysis.HarmonicAnalysis(self.songs,1)
        
        self.tempo_list = []
        self.tempo_stats = {}
        for song in self.songs:
            self.tempo_list.append(song.bpm)

        self.tempo_stats["mean"] = statistics.mean(self.tempo_list)
        self.tempo_stats["median"] = statistics.median(self.tempo_list)
        self.tempo_stats["min"] = min(self.tempo_list)
        self.tempo_stats["max"] = max(self.tempo_list)
        self.tempo_stats["stdev"] = statistics.stdev(self.tempo_list)

        self.harmony_length_list = []
        for song in self.songs:
            song_chord_length = []
            for segment in song.segments:
                for chord in segment.chords:
                    song_chord_length.append(chord.chord_duration)
            self.harmony_length_list.append(song_chord_length)

        self.harmony_means = []
        for stats in self.harmony_length_list:
            self.harmony_means.append(statistics.mean(stats))

        #print(self.harmony_means)

        bleh = []
        for i in self.songs:
            bleh.append(i.title)
            #print(i.title)
        #print(bleh)

        #print(self.tempo_list)
        #print(self.harmony_means)
        trace = go.Scatter(x=self.tempo_list,y=self.harmony_means, mode='markers', text=bleh)
        data = [trace]
        #plotly.offline.plot(data, filename='DATA')
       # print(self.harmony_length_list)

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

    def get_gestures_in_corpus(self,gesture_cutoff=1,reverse=False):
        #print()
        return self.melody_model.get_gestures_in_corpus(gesture_cutoff,reverse)
    
    def generate_harmonic_rhythm(self):
        return self.harmonic_model.generate_rhythm_vector()

    def calculate_statistics(self):
        return self.harmonic_model.get_statistics()

    def get_solfege_histogram(self):
        self.melody_model.get_histogram()

    #Does song tempo influence chord length?
    def get_tempo_stats(self):
        return self.tempo_stats

    def graph_tempo_hist(self):
        data = [go.Histogram(x=self.tempo_list)]
        plotly.offline.plot(data, filename='Tempos')
            
