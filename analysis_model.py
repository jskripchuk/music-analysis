import melodic_analysis
import harmonic_analysis
import tools

class CorpusAnalysis:
    def __init__(self, filepath):
        self.songs = tools.get_corpus_list(filepath)
        self.melody_model = melodic_analysis.MelodicAnalysis(self.songs,1,0.5)
        self.harmonic_model = harmonic_analysis.HarmonicAnalysis(self.songs,1)


    def generate_progression(self):
        return self.harmonic_model.markov_model.make_sentence()

    def generate_melodic_sequence(self):
        return self.melody_model.markov_model.make_sentence()

    def generate_harmonic_rhythm(self):
        return self.harmonic_model.generate_rhythm_vector()

    def calculate_statistics(self):
        return self.harmonic_model.get_statistics()
