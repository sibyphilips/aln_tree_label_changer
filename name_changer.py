#!/usr/bin/python3
import re
import shutil
import string
import os
import fileinput
import csv
import pandas as pd
##
#improved on the 22nd of October 2017 with changes to short string replacement in fasta headers of semi identical long names
##

print("\n\n\n\nTHIS SCRIPT IS USED TO CHANGE FASTA HEADERS OR TREE TIP NAMES ACCORDING TO THE USERS NEEDS \n usually we need to shorten names to less than TEN characters for phylogenetics programmes \n like PAML,PHYML,PHYLIP etc. Once we change the fasta name it may be essential to change a tree tip names as well.\nSiby Philip\n7th April 2022\n\n")

print( "#####\n#v0.2022_04_07_01\n#####")
#Raw_input is used to collect data from the user
Ch_for = input('=====what is your file, enter 1 for fasta and 2 for newick=====:     ')
file_in = input('\n====please enter the file name below====: ')


rtable = input('\n===Please provide the replacement table file with exactly 2 columns in csv format===:   ')

#fval = input('\n==From first column to which column == : ')
output = input('\n=What file name for output=: ')

#fvalue=int(fval)-2
#numb=int(fvalue)
replace_file = pd.read_csv(rtable,header=None,sep=",")#give \t instead of comma for tsv files
replace_file.columns = ["species_names","replace_names"]

#if we need only a few columns from a pandas file for example if the pandas file has many columns append the format above to change the headers, then use as in the following example to take only the needed columns

#age_sex = replace_file[["Age", "Sex"]]
replace_dict = replace_file.set_index("species_names")["replace_names"].to_dict()




#making dictionary from csv file
#ref:https://stackoverflow.com/questions/14091387/creating-a-dictionary-from-a-csv-file###

##rtable = {}
#for row in reader:
 #   key = row[0]
  #  if key in rtable:
        # implement your duplicate row handling here
    #    pass
   # rtable[key] = row[1:]
#print rtable

#lets start the loop here for header_change
#using the dictionary to change the header lines
#ref: https://stackoverflow.com/questions/43139174/replacing-words-in-text-file-using-a-dictionary

def fasta_header_ch(file_in):
    i=0
    with open(file_in, 'r') as input_file, open(output, 'w') as output_file:
        for line in input_file:
            if '>' in line:
                lin = line.rstrip()#we are taking the fasta header
                ll=lin.split(">")
                nlin=ll[1]
	        #print str(lin)
                fas = '>'
                output_file.write(fas)
            #if not line:
                #continue
                for f_key, f_value in replace_dict.items():
                #print f_key
                #print f_value
                    if f_key == nlin:
		        #lin = lin.replace(str(f_key), str(f_value[int(fvalue)]))
                    #nlin = nlin.replace(f_key, str(f_value))
                        nlin = re.sub(r'\b' + f_key + r'\b', f_value, nlin)
				#trial to remove a bug which removes shorter fkeys within longer fkeys with the shorter ones fvalue
                    #nnlin=fas+nlin
                    #print(nnlin)
                output_file.write(nlin) #we are replacing the new file's line with our new header
                output_file.write('\n')
            else:
                output_file.write(line)
        i=i+1
    output_file.close()



def TreeNCh(tree):
    i=0
    with open(file_in, 'r') as input_file, open(output, 'w') as output_file:
        for line in input_file:
            tlin = line.rstrip()#we are reading the tree tips
            #ntlin = line.split(',')
            print(tlin)
            for f_key, f_value in replace_dict.items():
                if f_key in tlin:
		    #lin = lin.replace(str(f_key), str(f_value[int(fvalue)]))
                    tlin = re.sub(r'\b' + f_key + r'\b', f_value, tlin)
                    #lin = lin.replace(f_key, f_value[numb])#trial to remove a bug which removes shorter fkeys within longer fkeys with the shorter ones fvalue
                    #print(lin)
            output_file.write(tlin) #we are replacing the new file's line with our new header
            output_file.write('\n')
        else:
            pass
        i=i+1
    output_file.close()

if Ch_for == "1":
    fasta_header_ch(file_in)

elif Ch_for == "2":
    TreeNCh(file_in)

