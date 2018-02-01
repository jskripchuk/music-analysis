import analysis_model as analysis

#obj = analysis.HarmonicAnalysis("data-files/porter_robinson",1)
#obj = analysis.MelodicAnalysis("data-files/adele_example/HKT_files_chorus",1,0.5)
#print(obj.generate_line())
#print(obj.gestures_in_corpus)
#print(obj.gestures_in_corpus)
obj = analysis.CorpusAnalysis("data-files/adele_example/HKT_files_chorus")
print(obj.generate_progression())
#print(obj.markov_model.to_dict())
