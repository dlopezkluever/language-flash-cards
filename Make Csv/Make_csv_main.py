import pandas
### Takes wordlist data from https://github.com/hermitdave/FrequencyWords/blob/master/content/2018/de/de_50k.txt
### and turns into nice csv, to then translate on google sheets. https://docs.google.com/spreadsheets/d/1mXkiiq-om27gKvo0MO6a4hHOCV-NpzmJ9beUo1p-60s/edit?gid=0#gid=0
with open("de_50k.txt", "r") as retard_file:
    lines = retard_file.readlines()
new_wordlist = []
whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
for item in lines:
    # only_word= ""
    only_word= "".join(filter(whitelist.__contains__, item))
    new_wordlist.append(only_word)
# print(new_wordlist)

#NOTE: Change the amount of words you want in your file. There's 50k originally, I only want 1k
limit_wordlist = [new_wordlist[i] for i in range(0,1000)]

data_frame= pandas.DataFrame(limit_wordlist)
data_frame.to_csv("Clean_German.csv", header=False)


