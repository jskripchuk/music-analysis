import harmonic_analysis as analysis

obj = analysis.HarmonicAnalysis("data-files/porter_robinson",1)

#print(obj.generate_progression())
print(obj.rhythm_array)
#print(obj.rhythm_array)
#print(obj.chords_per_measure_tuple)
print(obj.generate_rhythm_vector())
