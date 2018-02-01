import markovify
file_object = open("form_corpus.txt","r")
file_text = file_object.read()
model = markovify.Text(file_text, state_size=1)


for i in range(0,10):
    print(model.make_short_sentence(140))

##TODO
#Does not register newline characters as new line
