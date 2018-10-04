import analysis_model as analysis
import hkt_generator as g
import os
#os.chdir("C:\\Users\\Jimmy\\Documents\\GitHub\\music-analysis")
print(os.getcwd())

filepath = os.getcwd()+"/pokemon.json"

#obj = g.HKTObject(filepath)


#mem = analysis.HarmonicAnalysis()
#print(obj.segments[0].chords[0])
obj = analysis.CorpusAnalysis("test",1)
#obj = analysis.MelodicAnalysis("data-files/adele_example/HKT_files_chorus",1,0.5)
#print(obj.generate_line())
#print(obj.generate_progression())

#print(obj.gestures_in_corpus)
#print(obj.gestures_in_corpus)
#obj = analysis.CorpusAnalysis("zedd_files")
#obj.calculate_statistics()
#print(obj.generate_progression())
#print(obj.generate_harmonic_rhythm())
print(obj.generate_melodic_sequence())
#print(obj.markov_model.to_dict())
