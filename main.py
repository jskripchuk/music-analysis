import analysis_model as analysis
import hkt_generator as g
import os
#os.chdir("C:\\Users\\Jimmy\\Documents\\GitHub\\music-analysis")
#print(os.getcwd())

filepath = os.getcwd()+"/adele"
obj = analysis.CorpusAnalysis(filepath)

#print(obj.generate_line())
print(obj.generate_progression())
print(obj.get_gestures_in_corpus())
print(obj.generate_melodic_sequence())
print(obj.generate_harmonic_rhythm())
print(obj.get_tempo_stats)
obj.calculate_statistics()
obj.get_melody_histograms()
#print(obj.generate_progression())
#print(obj.generate_melodic_sequence())
#rest = 0.25






# for i in (0.25,0.5,1,1.5):
#     print("#######################")
#     print("Gesture Rest of "+str(i))
#     print("#######################")
#     #print("Forward ")
#     st = obj.get_gestures_in_corpus(i)
#     #print("Rev")
#     rev = obj.get_gestures_in_corpus(i, True)
#     print("Forward: " +str(st))
#     print("Reverse: "+str(rev))
#     average = []

#     for i in range(0,3):
#         average.append( (st[i]+rev[i])/2 )
#     print("Average: "+str(average))
#     print("-----------------------------------")
    
    
#print(obj.generate_harmonic_rhythm())
#print(obj.get_gestures_in_corpus())
#print(obj.get_tempo_stats())

#print(obj.gestures_in_corpus)
#print(obj.gestures_in_corpus)
#obj = analysis.CorpusAnalysis("zedd_files")
#obj.get_solfege_histogram()
#print(obj.markov_model.to_dict())
