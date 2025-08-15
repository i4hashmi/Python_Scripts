#!/home/hashmi/psi4conda/bin/python3
# 
# energy.py
#
# python script to extract the SCF energy for each step, find the lowest energy step
# and produce a quick graph showing the change in energy in kJ/mol
# to run the script type 
# python energy.py input_file_name 
# NOTE you can close the graph by pressing "q" on keyboard
#
import sys
import numpy as np
import matplotlib.pyplot as plt
import os
dir=os.getcwd()
#
# setup files to read
if len(sys.argv) == 1:
  print('to run the script please type: python energy.py input_file_name')
  sys.exit()
else:
  log_file=str(sys.argv[1])
  s='directory is '
  print('{0:}{1:}'.format(s,dir))
  s='input file is '
  print('{0:}{1:}'.format(s,log_file))
#close if

# open the file
f = open(log_file,'r')

# set some basic parameters
energy=[]
new_energy=[]
x_axis=[]
en_search_string='SCF Done:'

# read the if there is a first line, then read the file line by line
# if energy is given split the line into array tmp and extract the energy number
# and extract the energy and store in an array
count=0
line=f.readline()
while line:
  line =f.readline()
#  print('{0:}'.format(line))
  if en_search_string in line:
    tmp=line.rstrip().split()
    energy.append(float(tmp[4]))         
    count1=count+1
    print('{0:}{1:<3}{2:<.8f}'.format('step: ',count1,energy[count]))
    count=count+1
# endif
#endwhile

total_steps=count
#print(total_steps)

# find the lowest energy
min_energy=min(energy)
min_index=energy.index(min(energy))
print('{0:}{1:}{2:}{3:}'.format('lowest energy is step: ',min_index+1,'  energy: ',min_energy))

# convert to kJ/mol relative to lowest energy
# create x_axis which starts numbering at 1, remember python starts at zero
x=0
while x < total_steps :
  temp=(energy[x] - min_energy) * 2625.5
  new_energy.append(temp)
  x=x+1
  x_axis.append(x)
#endwhile

# plot the energy
plt.plot(x_axis,new_energy,'b-')
plt.plot(x_axis,new_energy,'bo')
plt.plot(min_index+1,new_energy[min_index],'rs',markersize=8)
plt.ylabel('energy kJ/mol')
plt.xlabel('step')
plt.show()

# close file
f.close()
#sys.exit()
#end