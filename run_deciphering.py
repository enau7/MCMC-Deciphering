import matplotlib.pyplot as plt
from metropolis_hastings import *
import shutil
from deciphering_utils import *
import pandas as pd

#!/usr/bin/python

import sys
from optparse import OptionParser

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

def main(argv):
   inputfile = None
   decodefile = None
   parser = OptionParser()

   parser.add_option("-i", "--input", dest="inputfile", 
                     help="input file to train the code on")
   
   parser.add_option("-d", "--decode", dest="decode", 
                     help="file that needs to be decoded")
   
   parser.add_option("-e", "--iters", dest="iterations", 
                     help="number of iterations to run the algorithm for", default=5000)
    
   parser.add_option("-t", "--tolerance", dest="tolerance", 
                     help="percentate acceptance tolerance, before we should stop", default=0.02)
   
   parser.add_option("-p", "--print_every", dest="print_every", 
                     help="number of steps after which diagnostics should be printed", default=10000)

   (options, args) = parser.parse_args(argv)

   filename = options.inputfile
   decode = options.decode
   
   if filename is None:
      print("Input file is not specified. Type -h for help.")
      sys.exit(2)

   if decode is None:
      print("Decoding file is not specified. Type -h for help.")
      sys.exit(2)

   char_to_ix, ix_to_char, tr, fr = compute_statistics(filename)
   
   s = list(open(decode, 'r').read())
   scrambled_text = list(s)
   i = 0
   initial_state = get_state(scrambled_text, tr, fr, char_to_ix)
   states = []
   entropies = []
   while i < 3:
      iters = options.iterations
      print_every = int(options.print_every)
      tolerance = options.tolerance
      state, lps, _ = metropolis_hastings(initial_state, proposal_function=propose_a_move, log_density=compute_probability_of_state, 
                                            iters=iters, print_every=print_every, tolerance=tolerance, pretty_state=pretty_state)
      states.extend(state)
      entropies.extend(lps)
      i += 1
      #if(i<3): input("\n Starting in a new Random State...")

   
   p = list(zip(states, entropies))
   p.sort(key=lambda x:x[1])
   
   print(" Best Guesses : \n")
   
   for j in range(1,4):
      print(f"Guess {j}: \n")
      print(pretty_state(p[-j][0], full=True))
      print(shutil.get_terminal_size().columns*'*')

   bestguess = pretty_state(p[-1][0],full=True) # Gets the best guess
   with open("modData/frequent_words.txt") as f:
     freq_words = [line.rstrip('\n') for line in f]

   output_map = {} # This will be a map that sends what we have now to what we thing the result should be.

   # First, we increment along to get a word.
   i = 0
   length = len(bestguess)
   while i < length:

      while (i < length) and (not bestguess[i].isalpha()):
         i += 1

      word = ""
      start_index = i

      while (i < length) and (bestguess[i].isalpha()):
         word += bestguess[i]
         i += 1
      
      end_index = i

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

      # We now have an upper-case word.

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


   print("Transformed Best Guess: \n")
   print(output)
         
               

   
if __name__ == "__main__":
   main(sys.argv)