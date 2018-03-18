import analysis_model as analysis

#obj = analysis.HarmonicAnalysis("data-files/porter_robinson",1)
#obj = analysis.MelodicAnalysis("data-files/adele_example/HKT_files_chorus",1,0.5)
#print(obj.generate_line())
#print(obj.gestures_in_corpus)
#print(obj.gestures_in_corpus)
obj = analysis.CorpusAnalysis("data-files/adele_example/HKT_files_chorus")
obj.calculate_statistics()
print(obj.generate_progression())
print(obj.generate_harmonic_rhythm())
#print(obj.markov_model.to_dict())
