import csv

with open('billboard_by_artist.csv', 'rt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    list_artists = []
    num_songs = []
    current_count = 0
    current_artist =""
    lim = 4
    for row in spamreader:
        if row[5] == current_artist:
            current_count+=1
        else:
            #print(current_count)
            if current_count > lim:
                list_artists.append(current_artist)
                num_songs.append(current_count)
            current_artist = row[5]
            current_count = 1


    for i in range(0, len(num_songs)):
        print("%s : %s" % (list_artists[i], num_songs[i]))
        #print(row[5])
