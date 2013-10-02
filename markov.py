# open and read a file
# analyze the text: make a dictionary of tuples and lists
# then, generate sentences using markov chains

from sys import argv
import random
import twitter

capital_tuples = []
tweetThis = True

def normalize(filetext):

    filetext = filetext.replace("--"," ")
    
    list_of_words = filetext.split()

    for i in range(len(list_of_words)):
        list_of_words[i] = list_of_words[i].strip(",\-;:_/[]*$#0123456789%")

    return list_of_words

def create_dict(list_of_words):
    new_dict = {}

    for i in range(len(list_of_words)-2):

        first_word = list_of_words[i]

        tuple_to_add = (first_word, list_of_words[i+1])

        if "" not in tuple_to_add:
            if ord("A") <= ord(first_word[0]) <= ord("Z"):
                capital_tuples.append( tuple_to_add )

            new_dict.setdefault(tuple_to_add,[])
            new_dict[tuple_to_add].append(list_of_words[i+2])

    return new_dict

def tweetIt(tweet):
    if tweetThis:

        #if you want this to work again, fill in the secrets...
        api = twitter.Api(consumer_key='F8TPrToNh8pLTc0xqdQ', consumer_secret='', access_token_key='1925059322-zJO7EHV2d7lF64iOybPANZTG3mBxuni6Q9AtwUQ', access_token_secret='')

        api.PostUpdate(tweet)

def main():

    filetext = ""

    # this works in Linux where you can unpack multiple values from command line on the fly. argv might be script, filename or script, filename1, filename2, etc.
    for arg in argv[1:]:
        f = open(arg)
        filetext += f.read()
        f.close()

    list_of_words = normalize(filetext)
    markov_dict = create_dict(list_of_words)
    
    #Initialize sentence variable as empty string
    sentence = ""

    #Create first two words of the sentence by randomly picking an item that starts with a capital letter
    random_capital = random.choice(capital_tuples)

    #Initial tuple pair
    item_key = random_capital # this is a tuple

    #List of values associated with the tuple pair
    item_value = markov_dict[random_capital] # this is a list

    #Combine initial tuple pair with initial sentence variable
    sentence = item_key[0] + " " + item_key[1]

    #Long way of choosing my choice: 
    # rando = random.randint(0, len(item_value)-1)

    while len(sentence) <= 140:
        #pick random word from the list associated with the tuple key
        next_value = random.choice(item_value)

        #add random word to the sentence
        if len(sentence + " " + next_value) > 139:
            break

        sentence = sentence + " " + next_value

        #Create next tuple with second value in the item key plus next_value
        next_tuple = (item_key[1],next_value)

        # if key in dictionary, keep going, otherwise we're at the end so stop.
        if next_tuple in markov_dict:
            item_key = next_tuple
            item_value = markov_dict[next_tuple]
        else:
            break

    ending_punc = ['.','!','?']
    reversed_sentence = sentence[::-1]

    for i in range(len(sentence)-1):
        a_char = reversed_sentence[i]
        if a_char in ending_punc:
            sentence = sentence[:len(sentence)-i+1]
            break
        
    print sentence

    tweetIt(sentence)

main()