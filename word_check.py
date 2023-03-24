
def weight_dict_update(d, key, value):
   if not (key in d.keys()):
      d[key] = []
   d[key] += [value]

def getmode(lst):
   outdict = dict()
   for k in lst: # initialize dict with zeros
      outdict[k] = 0
   for k in lst: # increment
      outdict[k] += 1
   # return most frequent element
   return sorted(outdict.keys(), key = lambda x: outdict[x], reverse=True)[0]

def word_check_transform(bestguess, file = "modData/frequent_words.txt"):
    with open(file) as f:
        freq_words = [line.rstrip('\n') for line in f]

    output_map = {} # This will be a map that sends what we have now to what we think the result should be.

    # First, we increment along to get a word.
    i = 0
    length = len(bestguess)
    while i < length:

        while (i < length) and (not bestguess[i].isalpha()):
            i += 1

        word = ""

        while (i < length) and (bestguess[i].isalpha()):
            word += bestguess[i]
            i += 1
        
        if word == "":
            break
        
        if not word[0].isupper():
            continue
        
        # If the word we pass in is already an english word, 
        # it's probably a bad idea to make the swap, so i'll continue.
        
        # I will, however, add itself as a weight to the final dictionary.
        if word.lower() in freq_words:
            weight_dict_update(output_map, word[0], word[0])
            continue

        # We now have a capitalized word.

        for check in freq_words:
            if word[1:] == check[1:]:
                weight_dict_update(output_map, word[0], check[0].upper())

    # Now, we our dictionary. We just need to send the values we have to the values we expect.

    output = ""
    for k in bestguess:
        if k not in output_map.keys():
            output += k
        else:
            output += getmode(output_map[k])

    return output