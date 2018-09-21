import os 
import json
import codecs
dir_path = os.path.dirname(os.path.realpath(__file__))

#JSon uses UTF-8 BOM Header (??????)

filename = "pokemon.json"
file_path = dir_path+"/"+filename

#print(file_path)

#data = open(file_path).read()

#data = json.loads(data)

data = json.load(codecs.open(file_path,'r','utf-8-sig'))

#with open(file_path) as f:
   # data = json.load(f)
print(json.dumps(data, indent=4))
print(data["chords"])

#print(dir_path)