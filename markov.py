# open and read a file
# analyze the text: make a dictionary of tuples and lists
# then, generate sentences using markov chains

from sys import argv
import random

script, filename = argv

def normalize(filetext):

    filetext = filetext.replace("--"," ")
    
    list_of_words = filetext.split()

    for i in range(len(list_of_words)):
        list_of_words[i] = list_of_words[i].strip(".?,\"!-;:_()/[]*$#")

    return list_of_words

def create_dict(list_of_words):
    new_dict = {}

    for i in range(len(list_of_words)-2):
        tuple_to_add = (list_of_words[i], list_of_words[i+1])
        #try rewriting with setdefault
        new_dict[tuple_to_add] = new_dict.get(tuple_to_add,[])
        new_dict[tuple_to_add].append(list_of_words[i+2])

    return new_dict


def main():
    f = open(filename)
    filetext = f.read()

    list_of_words = normalize(filetext)
    markov_dict = create_dict(list_of_words)

    #print markov_dict
  
    #starting_index = randint(0,len(markov_dict.keys())-1)
    # print starting_index
    # print len(markov_dict.keys())
    
    #Initialize sentence variable as empty string
    sentence = ""

    #Create first two words of the sentence by randomly picking a tuple key
    starting_item = random.choice(markov_dict.items())

    #Initial tuple pair
    item_key = starting_item[0] # this is a tuple

    #List of values associated with the tuple pair
    item_value = starting_item[1] # this is a list

    #Combine initial tuple pair with initial sentence variable
    sentence = item_key[0] + " " + item_key[1]

    #Long way of choosing my choice: 
    # rando = random.randint(0, len(item_value)-1)

    while len(sentence) < 140:
        #pick random word from the list associated with the tuple key
        next_value = random.choice(item_value)

        #add random word to the sentence
        sentence = sentence + " " + next_value

        #Create next tuple with second value in the item key plus next_value
        next_tuple = (item_key[1],next_value)

        # if key in dictionary, keep going, otherwise we're at the end so stop.
        if next_tuple in markov_dict:
            item_key = next_tuple
            item_value = markov_dict[next_tuple]
        else:
            break

    print sentence
    # print markov_dict

main()