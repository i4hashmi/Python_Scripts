#! /usr/bin/python3

import numpy
import matplotlib.pyplot as plt
import os.path


print("#---------------------------------------------------------------------------------------------------#")
print("#---------------------------------------------------------------------------------------------------#")
print("#       A Script to Plot Different Optimization Energies against the Optimization Step Number       #")
print("#---------------------------------------------------------------------------------------------------#")
print("#---------------------------------------------------------------------------------------------------#")

# Take the input file in first argument
import sys
#with open(sys.argv[1], 'r') as f:
#input_file = 'c180_fullerene.out'
input_file = open(sys.argv[1])
#f = open(input_file, 'r')
lines = input_file.readlines()
filename=os.path.splitext(os.path.basename(sys.argv[1]))[0] # Take the Filename out to use as Title of the Graph

# Define a function to plot the graph from the extracted information
#---------- Start of Function ----------#
def Plot_the_Graph(x_axis, y_axis, title, x_axis_title, y_axis_title):
    plt.scatter(x_axis, y_axis)
    plt.plot(x_axis, y_axis)
    plt.suptitle(title, fontsize=22)
    plt.xlabel(x_axis_title, fontsize=18)
    plt.ylabel(y_axis_title, fontsize=18)
    #plt.show()
#---------- End of Function ----------#

#---------------------------------------------------------------#
# Finding Energy Change and Single Point Energy in Output File  #
#---------------------------------------------------------------#
Single_Point_Energies = []
Energies = []
RMS_gradient = []
Max_gradient = []
#---------- Start of Loop ----------#
for i, line in enumerate(lines):
    if 'Geometry convergence' in line:
        if 'Energy change' in lines[i+3]:
            complete_line = lines[i+3] # Take the 4th Line after the line containing Geometry Convergence
            splitted_line = complete_line.split() # Split the line with Energy Change
            energy_change = float(splitted_line[2]) # Save the Energy Change Value
            Energies.append(energy_change)
        else:
            Energies.append(0)
    if 'Geometry convergence' in line:
        if 'RMS gradient' in lines[i+3]:
            complete_line2 = lines[i+3] # Take the 4th Line after the line containing Geometry Convergence
            splitted_line2 = complete_line2.split() # Split the line with RMS gradient
            rms1 = float(splitted_line2[2]) # Save the RMS gradient Value
            RMS_gradient.append(rms1)
    if 'Geometry convergence' in line:
        if 'RMS gradient' in lines[i+4]:
            complete_line3 = lines[i+4] # Take the 4th Line after the line containing Geometry Convergence
            splitted_line3 = complete_line3.split() # Split the line with RMS gradient
            rms2 = float(splitted_line3[2]) # Save the RMS gradient Value
            RMS_gradient.append(rms2)
    if 'Geometry convergence' in line:
        if 'MAX gradient' in lines[i+4]:
            complete_line4 = lines[i+4] # Take the 4th Line after the line containing Geometry Convergence
            splitted_line4 = complete_line4.split() # Split the line with RMS gradient
            max1 = float(splitted_line4[2]) # Save the RMS gradient Value
            Max_gradient.append(max1)
    if 'Geometry convergence' in line:
        if 'MAX gradient' in lines[i+5]:
            complete_line5 = lines[i+5] # Take the 4th Line after the line containing Geometry Convergence
            splitted_line5 = complete_line5.split() # Split the line with RMS gradient
            max2 = float(splitted_line5[2]) # Save the RMS gradient Value
            Max_gradient.append(max2)
#---------- End of Loop ----------#

# Below is the variable to check the length of the Energies list and make a list for step numbers from 1 to len(Energies)
Step_Numbers = numpy.linspace(1, len(Energies), len(Energies))

#----------------------------------------------------#
# Finding Final Single Point Energy in Output File   #
#----------------------------------------------------#
#---------- Start of Loop ----------#
for i in lines:
    if 'SCF NOT CONVERGED AFTER' in i:
        break
    if 'FINAL SINGLE POINT ENERGY' in i:
        complete_line6 = i.split()
        final_energy = float(complete_line6[4])
        Single_Point_Energies.append(final_energy)
    if 'THE OPTIMIZATION HAS CONVERGED' in i:
        break
#---------- End of Loop ----------#
#----------------------------------------------------#
#-------------------------------------------#
#         Labels for Axis of Graphs         #
#-------------------------------------------#
# Labels for axis
x_axis_label_energy_change = 'Optimization Step Number'
y_axis_label_energy_change = 'Energy Change'
y_axis_label_rms_gradient = 'RMS Gradient'
y_axis_label_single_point_E = 'Single Point E'
y_axis_label_max_gradient = 'MAX Gradient'
#----------------------------------------------------#


#-------------------------------------------#
# Plot the Graphs in a 2X2 matrix fashion   #
#-------------------------------------------#
fig = plt.figure()
ax1 = fig.add_subplot(221)
ax1.plot = Plot_the_Graph(Step_Numbers, Single_Point_Energies, filename, x_axis_label_energy_change, y_axis_label_single_point_E)
ax2 = fig.add_subplot(222)
ax2.plot = Plot_the_Graph(Step_Numbers, Energies, filename, x_axis_label_energy_change, y_axis_label_energy_change)
ax3 = fig.add_subplot(223)
ax3.plot = Plot_the_Graph(Step_Numbers, RMS_gradient, filename, x_axis_label_energy_change, y_axis_label_rms_gradient)
ax4 = fig.add_subplot(224)
ax4.plot = Plot_the_Graph(Step_Numbers, Max_gradient, filename, x_axis_label_energy_change, y_axis_label_max_gradient)
plt.show()
#----------------------------------------------------#

print('Optimization Step Numbers: ', Step_Numbers, '\n')
print('Single Point Energies: ', Single_Point_Energies, '\n')
print('Length of Single Point Energies', len(Single_Point_Energies), '\n')
print('Energy Change: ', Energies, '\n')
print('Length of Energies', len(Energies), '\n')
print('RMS Gradient: ', RMS_gradient, '\n')
print('Length of RMS Gradient', len(RMS_gradient), '\n')
print('MAX Gradient: ', Max_gradient, '\n')
print('Length of Max Gradient', len(Max_gradient), '\n')


'''
# ASCII FONTS from: http://patorjk.com/software/taag/
# Font = "Big", "Ivrit"
print("#==================================================================#")
print("#------------------------------------------------------------------#")
print('#  _____                 _                      _     _            #')
print('# |  __ \               | |                    | |   | |           #')
print('# | |  | | _____   _____| | ___  _ __   ___  __| |   | |__  _   _  #')
print("# | |  | |/ _ \ \ / / _ \ |/ _ \| '_ \ / _ \/ _` |   | '_ \| | | | #")
print('# | |__| |  __/\ V /  __/ | (_) | |_) |  __/ (_| |   | |_) | |_| | #')
print('# |_____/ \___| \_/ \___|_|\___/| .__/ \___|\__,_|   |_.__/ \__, | #')
print('# | |  | |         | |          | |(_)                       __/ | #')
print('# | |__| | __ _ ___| |__  _ __ _|_| _                       |___/  #')
print("# |  __  |/ _` / __| '_ \\| '_ ` _ \| |                             #")
print('# | |  | | (_| \__ \ | | | | | | | | |                             #')
print('# |_|  |_|\__,_|___/_| |_|_| |_| |_|_|                             #')
print("#------------------------------------------------------------------#")
print("#==================================================================#")'''
