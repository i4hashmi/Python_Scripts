#! /usr/bin/python3

""" This is a general purpose SCF progress plotting script for Gaussian or ORCA output files.
    It takes a Gaussian or ORCA ouput file, determines which file it is, and then plots the
    Single point energy, Energy change, RMS Gradient, and Max Gradient vs the Optimization Step Number.

    Written by Muhammad Ali Hashmi, Victoria University of Wellington, 2017. """

import numpy
import matplotlib.pyplot as plt
import sys

print("#---------------------------------------------------------------------------------------------------#")
print("#---------------------------------------------------------------------------------------------------#")
print("#       A Script to Plot Different Optimization Energies against the Optimization Step Number       #")
print("#---------------------------------------------------------------------------------------------------#")
print("#---------------------------------------------------------------------------------------------------#")

#############################################################################################################
# This section is for the definition of Dictionaries, Classes, Functions etc.
#############################################################################################################

#--------------------------------------------------------------------#
# Define a function to plot the graph from the extracted information #
#--------------------------------------------------------------------#
#---------- Start of Function ----------#
def Plot_the_Graph(x_axis, y_axis, title, x_axis_title, y_axis_title):
    plt.scatter(x_axis, y_axis)
    plt.plot(x_axis, y_axis)
    plt.suptitle(title, fontsize=22)
    plt.xlabel(x_axis_title, fontsize=18)
    plt.ylabel(y_axis_title, fontsize=18)
    #plt.show()
#---------- End of Function ----------#

#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+#
# A Class for Extracting the SCF Steps and their Parameters from a Gaussian or ORCA ouput File #
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Start of Class %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
class ExtractSCF(object):
    """A Class for Extracting the SCF Steps and their Parameters from a Gaussian or ORCA ouput File"""
    def __init__(self, file):
        self.file = file

    #------------------------------------------------------------------------------#
    # Define a function to read the input file and extract the SCF Steps info etc. #
    #------------------------------------------------------------------------------#
    #----------------------------- Start of Function -----------------------------#
    def extractSCF(self, file):
        #print("\nExtracting the Molecule from the given output file")
        f = open(file, 'r')
        program = "N/A"
        # Determine if we're dealing with Gaussian09 or ORCA
        for line in f:
            if line.find("Entering Gaussian System, Link 0=g09") != -1 or line.find("Copyright (c) 1988,1990,1992,1993,1995,1998,2003,2009, Gaussian, Inc.") != -1:
                print("Reading Gaussian output file: ", file, '\n')
                program = "g09"
                break
            elif line.find("* O   R   C   A *") != -1:
                print("Reading ORCA output file: ", file, '\n')
                program = "orca"
                break
        f.close()

        #---------------------------------------------------------------#
        # Finding Energy Change and Single Point Energy in Output File  #
        #---------------------------------------------------------------#
        Single_Point_Energies = []
        Energies = []
        RMS_gradient = []
        Max_gradient = []

        # Read through the ORCA output file
        #---------------------------------------------------------------#
        if program == "orca":
            f = open(file, 'r')
            lines = f.readlines()
            #---------------------------------------------------------------#
            # Finding Energy Change and Single Point Energy in Output File  #
            #---------------------------------------------------------------#
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
                if 'FINAL SINGLE POINT ENERGY' in line:
                    complete_line6 = line.split()
                    final_energy = float(complete_line6[4])
                    Single_Point_Energies.append(final_energy)
            #---------- End of Loop ----------#
            #----------------------------------------------------#
            return Single_Point_Energies, Energies, RMS_gradient, Max_gradient
            f.close()

        #---------------------------------------------------------------#
        # Read through the Gaussian output file
        #---------------------------------------------------------------#
        elif program == "g09":
            f = open(file, 'r')
            lines = f.readlines()
            #---------------------------------------------------------------#
            # Finding Energy Change and Single Point Energy in Output File  #
            #---------------------------------------------------------------#
            #---------- Start of Loop ----------#
            for i, line in enumerate(lines):
                if 'SCF Done' in line:
                    complete_line = line # Take the line containing SCF Done
                    splitted_line = complete_line.split() # Split the line with SCF Energy
                    SCF_energy = float(splitted_line[4]) # Save the SCF Energy Value
                    Single_Point_Energies.append(SCF_energy)
                if 'Predicted change in Energy' in line:
                    complete_line = line # Take the line containing the Energy Change
                    splitted_line2 = complete_line.split() # Split the line with SCF Energy
                    splitted_line2_split = splitted_line2[3].split("Energy=")[-1] # Take the value after Energy=
                    energy_value = float(splitted_line2_split[:splitted_line2_split.find("D")]) # Take the number before D
                    power = int(splitted_line2_split.split("D")[1]) # Take the power which comes after D
                    Energies.append(energy_value**power) # Save the Energy Change Value
                if 'Item' in line and 'Value' in line and 'Threshold' in line:
                    complete_line3 = lines[i+2] # Take the 2nd Line after the line containing "Item Value Threshold"
                    complete_line4 = lines[i+1]
                    splitted_line3 = complete_line3.split() # Split the line with RMS Force
                    splitted_line4 = complete_line4.split() # Split the line with Maximum Force
                    rms = float(splitted_line3[2]) # Save the RMS Force Value
                    maximum = float(splitted_line4[2]) # Save the Maximum Force Value
                    RMS_gradient.append(rms)
                    Max_gradient.append(maximum)
            #---------- End of Loop ----------#
            #----------------------------------------------------#
            return Single_Point_Energies, Energies, RMS_gradient, Max_gradient
        f.close()
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% End of Class %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#========================================================================================#

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#


###############################################################################
#                                                                             #
#                    The Main Part of the Program Starts Here                 #
#                                                                             #
###############################################################################



#input_file = 'Test_Files/C80-C240_fullerene.out' # Specify the input file here
#input_file = 'Test_Files/ev-2R3S-conf01.log' # Gaussian ouput file
input_file = sys.argv[1] # Take the input file in first argument

# Take the Filename out to use as Title of the Graph
filename = input_file.split('\\').pop().split('/').pop().rsplit('.', 1)[0]

# Run the class ExtractSCF in a variable molecule
molecule = ExtractSCF(input_file)
Single_Point_Energies, Energies, RMS_gradient, Max_gradient = molecule.extractSCF(input_file)

# Below is the variable to check the length of the lists and make a list for step numbers from 1 to len(list)
Step_No_Energy_change = numpy.linspace(1, len(Energies), len(Energies))
Step_No_Single_point_E = numpy.linspace(1, len(Single_Point_Energies), len(Single_Point_Energies))
Step_No_RMS_gradient = numpy.linspace(1, len(RMS_gradient), len(RMS_gradient))
Step_No_Max_gradient = numpy.linspace(1, len(Max_gradient), len(Max_gradient))

#-------------------------------------------#
#         Labels for Axis of Graphs         #
#-------------------------------------------#
# Labels for axis
x_axis_label_energy_change = 'Optimization Step Number'
y_axis_label_energy_change = 'Energy Change'
y_axis_label_rms_gradient = 'RMS Gradient'
y_axis_label_single_point_E = 'Single Point E'
y_axis_label_max_gradient = 'MAX Gradient'
#-------------------------------------------#
#-------------------------------------------#
# Plot the Graphs in a 2X2 matrix fashion   #
#-------------------------------------------#
fig = plt.figure()
ax1 = fig.add_subplot(221)
ax1.plot = Plot_the_Graph(Step_No_Single_point_E, Single_Point_Energies, filename, x_axis_label_energy_change, y_axis_label_single_point_E)
ax2 = fig.add_subplot(222)
ax2.plot = Plot_the_Graph(Step_No_Energy_change, Energies, filename, x_axis_label_energy_change, y_axis_label_energy_change)
ax3 = fig.add_subplot(223)
ax3.plot = Plot_the_Graph(Step_No_RMS_gradient, RMS_gradient, filename, x_axis_label_energy_change, y_axis_label_rms_gradient)
ax4 = fig.add_subplot(224)
ax4.plot = Plot_the_Graph(Step_No_Max_gradient, Max_gradient, filename, x_axis_label_energy_change, y_axis_label_max_gradient)
plt.show()
#----------------------------------------------------#

'''
print('Optimization Step Numbers: ', Step_No_RMS_gradient, '\n')
print('Single Point Energies: ', Single_Point_Energies, '\n')
print('Length of Single Point Energies', len(Single_Point_Energies), '\n')
print('Energy Change: ', Energies, '\n')
print('Length of Energies', len(Energies), '\n')
print('RMS Gradient: ', RMS_gradient, '\n')
print('Length of RMS Gradient', len(RMS_gradient), '\n')
print('MAX Gradient: ', Max_gradient, '\n')
print('Length of Max Gradient', len(Max_gradient), '\n')'''



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
print("#----------------- Email: i4hashmi@hotmail.com --------------------#")
print("#==================================================================#")
