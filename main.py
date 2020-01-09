import analysis_model as analysis
import os

filepath = os.getcwd()+"/adele"
obj = analysis.CorpusAnalysis(filepath)

print(obj.generate_progression())
print(obj.get_gestures_in_corpus())
print(obj.generate_melodic_sequence())
print(obj.generate_harmonic_rhythm())
print(obj.get_tempo_stats())

#obj.calculate_statistics()
#obj.get_melody_histograms()
#print(obj.generate_progression())
#print(obj.generate_melodic_sequence())
