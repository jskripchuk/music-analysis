import markovify
file_object = open("form_data.txt","r")
file_text = file_object.read()
model = markovify.Text(file_text, state_size=3)


for i in range(0,10):
    print(model.make_short_sentence(140))
