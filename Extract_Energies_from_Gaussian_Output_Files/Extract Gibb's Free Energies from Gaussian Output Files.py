#---------------------------------------------------------------------#
# A Script to Extract Gibb's Free Energies from Gaussian Output Files #
#---------------------------------------------------------------------#
from pylab import *
import glob
import re
import sys
import fileinput

print("A Script to Extract Gibb's Free Energies from Gaussian Output Files\n")

#Define the user input for input files (log files)
input_files = input('Enter the names of input files or a range (e.g. *.log):  ')

#Define a variable to ask for the output filename and add .txt extension automatically
output = open(input('Enter the name of output file to save the energies to:  ')+'.txt', 'w')

#Define a function which can find and copy the lines from log files containing Gibb's Free Energies

def gibbs_free_energies():
    for files in glob.glob(input_files):   #It takes all the files from user input defined above the function.
        read_file = open(files, "r")       #Reads the input files one by one
        input = read_file.readlines()      #Reads the files line by line and stores into a variable "input"
        output.write(files)                #Writes the name of the output file under processing
        output.write('\n')
        for line in input:                 #A loop to go through the file and find the match of the stated line
            if re.match("(.*)(S|s)um of electronic and thermal Free Energies(.*)", line):
                output.write(line)         #Writes the line found into the ouput file defined by the user
                output.write('\n')
    read_file.close()
    output.close()

gibbs_free_energies()

#------------------------------------------#
# Program by Muhammad Ali Hashmi   #
#------------------------------------------#
