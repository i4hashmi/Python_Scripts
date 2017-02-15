#! /usr/bin/python3
import numpy
import math
import sys

print("#-----------------------------------------------------------#")
print("#-----------------------------------------------------------#")
print("#     A Script to Find the Diameter of a Fullerene Cage     #")
print("#-----------------------------------------------------------#")
print("#-----------------------------------------------------------#")

# ASCII FONTS from: http://patorjk.com/software/taag/
# Font = "Big", "Ivrit"
'''
  _____                 _                      _     _
 |  __ \               | |                    | |   | |
 | |  | | _____   _____| | ___  _ __   ___  __| |   | |__  _   _
 | |  | |/ _ \ \ / / _ \ |/ _ \| '_ \ / _ \/ _` |   | '_ \| | | |
 | |__| |  __/\ V /  __/ | (_) | |_) |  __/ (_| |   | |_) | |_| |
 |_____/ \___| \_/ \___|_|\___/| .__/ \___|\__,_|   |_.__/ \__, |
 | |  | |         | |          | |(_)                       __/ |
 | |__| | __ _ ___| |__  _ __ _|_| _                       |___/
 |  __  |/ _` / __| '_ \| '_ ` _ \| |
 | |  | | (_| \__ \ | | | | | | | | |
 |_|  |_|\__,_|___/_| |_|_| |_| |_|_|

'''



#############################################################################################################
# This section is for the definition of *all* dictionaries and conversion factors
#############################################################################################################

# Conversion of length in Angstroms to  to
# atomic units (Bohrs)
def Ang2Bohr(ang):
    return ang*1.889725989

# Same in reverse
def Bohr2Ang(bohr):
    return bohr/1.889725989

# Dictionary to convert atomic symbols to atomic masses

SymbolToMass = {
"H" : 1.00794, "He": 4.002602, "Li": 6.941, "Be": 9.012182, "B": 10.811,
"C": 12.0107, "N": 14.0067, "O": 15.9994, "F": 18.9984032, "Ne": 20.1797,
"Na": 22.98976928, "Mg": 24.3050, "Al": 26.9815386, "Si": 28.0855,
"P": 30.973762, "S": 32.065, "Cl": 35.453, "Ar": 39.948, "K": 39.0983,
"Ca": 40.078, "Sc": 44.955912, "Ti": 47.867, "V": 50.9415, "Cr": 51.9961,
"Mn": 54.938045, "Fe": 55.845, "Co": 58.933195, "Ni": 58.6934, "Cu": 63.546,
"Zn": 65.38, "Ga": 69.723, "Ge": 72.64, "As": 74.92160, "Se": 78.96,
"Br": 79.904, "Kr": 83.798, "Rb": 85.4678, "Sr": 87.62, "Y": 88.90585,
"Zr": 91.224, "Nb": 92.90638, "Mo": 95.96, "Tc": 98.0, "Ru": 101.07,
"Rh": 102.90550, "Pd": 106.42, "Ag": 107.8682, "Cd": 112.411, "In": 114.818,
"Sn": 118.710, "Sb": 121.760, "Te": 127.60, "I": 126.90447, "Xe": 131.293,
"Cs": 132.9054519, "Ba": 137.327, "La": 138.90547, "Ce": 140.116,
"Pr": 140.90765, "Nd": 144.242, "Pm": 145.0, "Sm": 150.36, "Eu": 151.964,
"Gd": 157.25, "Tb": 158.92535, "Dy": 162.500, "Ho": 164.93032, "Er": 167.259,
"Tm": 168.93421, "Yb": 173.054, "Lu": 174.9668, "Hf": 178.49, "Ta": 180.94788,
"W": 183.84, "Re": 186.207, "Os": 190.23, "Ir": 192.217, "Pt": 195.084,
"Au": 196.966569, "Hg": 200.59, "Tl": 204.3833, "Pb": 207.2, "Bi": 208.98040,
"Po": 209.0, "At": 210.0, "Rn": 222.0, "Fr": 223.0, "Ra": 226.0, "Ac": 227.0,
"Th": 232.03806, "Pa": 231.03588, "U": 238.02891, "Np": 237.0, "Pu": 244.0,
"Am": 243.0, "Cm": 247.0, "Bk": 247.0, "Cf": 251.0, "Es": 252.0, "Fm": 257.0,
"Md": 258.0, "No": 259.0, "Lr": 262.0, "Rf": 267.0, "Db": 268.0, "Sg": 271.0,
"Bh": 272.0, "Hs": 270.0, "Mt": 276.0, "Ds": 281.0, "Rg": 280.0, "Cn": 285.0,
"Uut": 284.0, "Uuq": 289.0, "Uup": 288.0, "Uuh": 293.0, "Uuo": 294.0}


###############################################################################
#                                                                             #
#                    The Main Part of the Program Starts Here                 #
#                                                                             #
###############################################################################
# Function to read the input file
def read_input_file(input_filename):
    f = open(input_filename, 'r')
    fr = f.readlines()[2:] # [2:] at last means that it will read the file after second line as the coordinates start from 3rd line in an xyz file
    f.close()
    return fr

# To use the script in Terminal with input file in the first argument, uncomment below
# Take the input file as first argument
#input_file = sys.argv[1]

#coord = read_input_file(input('Enter the name of input file: '))
input_file = sys.argv[1]
#input_file = 'c20_fullerene.xyz'

# Read Input File. 'coord' is a list of all the xyz coordinates of the molecule
coord = read_input_file(input_file)



# This while loop asks you to enter a filename and if the name is not correct, then instead of crashing program, it asks you to enter a valid filename.
'''while True:
    try:
        coord = read_input_file(input('Enter the name of input file: '))
        break
    except FileNotFoundError:
        print("Please enter a valid filename with correct extension, e.g. ethane.xyz ! ")
    except:
        break
    finally:
        print("\n")'''

# Split the string coord into sublists.
for a in range(0,len(coord)):
    coord[a]=(coord[a].split())
# Convert numbers to floats
    for b in range(1,4):
        coord[a][b]=float(coord[a][b])

# Print (coord)
#print('\nThe xyz coordinates of the molecule under study are:\n')
#for i in range(0,len(coord)):
#    print("{:<3}  {: .8f}   {: .8f}   {: .8f}" .format(coord[i][0], coord[i][1], coord[i][2], coord[i][3]))

#-------------------------------------------------------#
# Calculation of Molecular center of mass (13-May-2015) #
#-------------------------------------------------------#

total_mass = 0
x = 0
y = 0
z = 0

for i in range(0, len(coord)):
    total_mass = total_mass+(SymbolToMass[coord[i][0]])
    x = x+((SymbolToMass[coord[i][0]])*(coord[i][1]))
    y = y+((SymbolToMass[coord[i][0]])*(coord[i][2]))
    z = z+((SymbolToMass[coord[i][0]])*(coord[i][3]))

x_cm = x/total_mass
y_cm = y/total_mass
z_cm = z/total_mass

# Below is the list containing the center of mass coordinates
cm_coords = [x_cm, y_cm, z_cm]
print('\n')
print("Center of mass coordinates = ", cm_coords)
print('\n')

#------------------------------------------------------#
# Calculation of Distance of Atoms from Center of Mass #
#------------------------------------------------------#

# Define a Function to Calculate the Distance between the center of mass and all the atoms in the list coords
def dist(atom1, atom2):
    dist = (atom1[1]-atom2[0])**2+(atom1[2]-atom2[1])**2+(atom1[3]-atom2[2])**2
    return math.sqrt(dist)

#Find the distance of every atom from the center of mass and append to the list defined below
Dist_from_CM = []

for i in range(0, len(coord)):
    Dist_from_CM.append(dist(coord[i], cm_coords))

#print(Dist_from_CM)

radius_of_fullerene = numpy.mean(Dist_from_CM)
diameter_of_fullerene = radius_of_fullerene * 2

print("Radius of the given Fullerene Cage is = ", radius_of_fullerene, "Angstrom")
print('\n')
print("Diameter of the given Fullerene Cage is = ", diameter_of_fullerene, "Angstrom")
print("Diameter of the given Fullerene Cage is = ", diameter_of_fullerene/10, "nm")

