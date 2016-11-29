import sys # Import sys to write to output files

print("#----------------------------------------------------------------------------------------------#")
print("#----------------------------------------------------------------------------------------------#")
print("#         Script to Extract the Optimized Structure from a Gaussian or ORCA output File        #")
print("#----------------------------------------------------------------------------------------------#")
print("#----------------------------------------------------------------------------------------------#")

# ASCII FONTS from: http://patorjk.com/software/taag/
# Font = "Big", "Ivrit"
def Stamp_Hashmi():
    print('\n')
    print(' _____                 _                      _     _')
    print('|  __ \               | |                    | |   | |')
    print('| |  | | _____   _____| | ___  _ __   ___  __| |   | |__  _   _')
    print("| |  | |/ _ \ \ / / _ \ |/ _ \| '_ \ / _ \/ _` |   | '_ \| | | |")
    print('| |__| |  __/\ V /  __/ | (_) | |_) |  __/ (_| |   | |_) | |_| |')
    print('|_____/ \___| \_/ \___|_|\___/| .__/ \___|\__,_|   |_.__/ \__, |')
    print('| |  | |         | |          | |(_)                       __/ |')
    print('| |__| | __ _ ___| |__  _ __ _|_| _                       |___/')
    print("|  __  |/ _` / __| '_ \| '_ ` _ \| |")
    print('| |  | | (_| \__ \ | | | | | | | | |')
    print('|_|  |_|\__,_|___/_| |_|_| |_| |_|_|')

    print("Dated: November 01, 2016\n")


#############################################################################################################
# This section is for the definition of dictionaries, functions etc.
#############################################################################################################

# A Dictionary to Convert Atomic Symbols to Atomic Numbers
SymbolToNumber = {
"H" :1, "He" :2, "Li" :3, "Be" :4, "B" :5, "C" :6, "N" :7, "O" :8, "F" :9,
"Ne" :10, "Na" :11, "Mg" :12, "Al" :13, "Si" :14, "P" :15, "S"  :16, "Cl" :17,
"Ar" :18, "K"  :19, "Ca" :20, "Sc" :21, "Ti" :22, "V"  :23, "Cr" :24,
"Mn" :25, "Fe" :26, "Co" :27, "Ni" :28, "Cu" :29, "Zn" :30, "Ga" :31,
"Ge" :32, "As" :33, "Se" :34, "Br" :35, "Kr" :36, "Rb" :37, "Sr" :38,
"Y"  :39, "Zr" :40, "Nb" :41, "Mo" :42, "Tc" :43, "Ru" :44, "Rh" :45,
"Pd" :46, "Ag" :47, "Cd" :48, "In" :49, "Sn" :50, "Sb" :51, "Te" :52,
"I"  :53, "Xe" :54, "Cs" :55, "Ba" :56, "La" :57, "Ce" :58, "Pr" :59,
"Nd" :60, "Pm" :61, "Sm" :62, "Eu" :63, "Gd" :64, "Tb" :65, "Dy" :66,
"Ho" :67, "Er" :68, "Tm" :69, "Yb" :70, "Lu" :71, "Hf" :72, "Ta" :73,
"W"  :74, "Re" :75, "Os" :76, "Ir" :77, "Pt" :78, "Au" :79, "Hg" :80,
"Tl" :81, "Pb" :82, "Bi" :83, "Po" :84, "At" :85, "Rn" :86, "Fr" :87,
"Ra" :88, "Ac" :89, "Th" :90, "Pa" :91, "U"  :92, "Np" :93, "Pu" :94,
"Am" :95, "Cm" :96, "Bk" :97, "Cf" :98, "Es" :99, "Fm" :100, "Md" :101,
"No" :102, "Lr" :103, "Rf" :104, "Db" :105, "Sg" :106, "Bh" :107,
"Hs" :108, "Mt" :109, "Ds" :110, "Rg" :111, "Cn" :112, "Uut":113,
"Fl" :114, "Uup":115, "Lv" :116, "Uus":117, "Uuo":118}

# Invert the Above: Atomic Numbers to Atomic Symbols
NumberToSymbol = {v: k for k, v in SymbolToNumber.items()}

#------------------------------------------------------------------------------#
# Define a function to extract the file name of the given file without extension #
#------------------------------------------------------------------------------#
#----------------------------- Start of Function -----------------------------#
def getFileName(file):
  return file.split('\\').pop().split('/').pop().rsplit('.', 1)[0]
#------------------------------ End of Function ------------------------------#

#------------------------------------------------------------------------------#
# Define a function to read the input file and extract the optimized structure #
#------------------------------------------------------------------------------#
#----------------------------- Start of Function -----------------------------#
def extractCoordinates(filename):
    #print("\nExtracting the Molecule from the given output file")
    f = open(filename, 'r')
    program = "N/A"
    # Determine if we're dealing with Gaussian09 or ORCA
    for line in f:
        if line.find("Entering Gaussian System, Link 0=g09") != -1 or line.find("Copyright (c) 1988,1990,1992,1993,1995,1998,2003,2009, Gaussian, Inc.") != -1:
            print("Reading Gaussian output file: ", filename, '\n')
            program = "g09"
            break
        elif line.find("* O   R   C   A *") != -1:
            print("Reading ORCA output file: ", filename, '\n')
            program = "orca"
            break
    f.close()

    # GEOMETRY READING SECTION
    geom = []
    # Read through Gaussian file, read "Standard orientation"
    if program == "g09":
        f = open(filename, 'r')
        for line in f:
            if line.find("Standard orientation:") != -1:
                del geom[:] # Delete a previous orientation if any and store the current one
                for i in range(0, 4):
                    readStructure = f.__next__() # Read the structure after 4th line from 'Standard Orientation'
                while True:
                    readStructure = f.__next__()
                    if readStructure.find("-----------") == -1: # Keep reading unless find ------
                        readStructure = readStructure.split()
                        geom.append(readStructure) # To append the current orientation to the list 'geom'
                        #print(readStructure)
                    else:
                        break
        # A Loop to delete the 1st and 3rd item of the list and convert 2nd item (Atomic Number) to Symbol
        for i in geom:
            del i[0:3:2]
            i[0] = NumberToSymbol[int(i[0])]
            i[1] = float(i[1]) # To convert the x coordinates from a string to floating number
            i[2] = float(i[2]) # To convert the y coordinates from a string to floating number
            i[3] = float(i[3]) # To convert the z coordinates from a string to floating number
        return geom
    # Read through ORCA file and find the Cartesian coordinates
    elif program == "orca":
        f = open(filename, 'r')
        for line in f:
            if line.find("CARTESIAN COORDINATES (ANGSTROEM)") != -1:
                del geom[:]
                readStructure = f.__next__()
                while True:
                    readStructure = f.__next__()
                    if readStructure and readStructure.strip():
                        readStructure = readStructure.split()
                        geom.append(readStructure)
                    else:
                        break
        # A Loop to convert the coordinates to floating point numbers
        for i in geom:
            i[1] = float(i[1])
            i[2] = float(i[2])
            i[3] = float(i[3])
        return geom
#------------------------------ End of Function ------------------------------#
#==============================================================================#

###############################################################################
#                                                                             #
#                    The Main Part of the Program Starts Here                 #
#                                                                             #
###############################################################################

# Specify the output file
#output_file = 'file_opt.log'
output_file = 'c60.out'

# Or take the input file in the first argument. Uncomment below if you want to use the script in linux with file in the first argument
#output_file = sys.argv[1]

# Get the file name of the given file to be used later
pure_filename = getFileName(output_file)

# Define a list to store the extracted structure from the output file
geometry = []

# Call the function on a list 'geometry' to save the coordinates of the extracted molecule in this list
geometry = extractCoordinates(output_file)
#print(geometry)

# Find the total number of atoms in the molecule
n_atoms = len(geometry)
print('The total number of atoms in the given molecule are:', n_atoms, '\n')

# Print the extracted coordinates
print('Here are the Cartesian coordinates of the optimized structure taken from the given output file:\n')
for i in geometry:
    print("{:<3}  {: .8f}  {: .8f}  {: .8f}".format(i[0], i[1], i[2], i[3]))

Stamp_Hashmi()

#========================================================================================#
#----------------------------------------------------#
# To write the new coordinates into a Gaussian file  #
#----------------------------------------------------#
#output_file = open(input('Enter the filename to write the new coordinates as Gaussian input: ')+'.com', "w")
output_file = open(pure_filename+'R'+'.gjf', 'w')
sys.stdout = output_file
#print('%nprocshared=24') #shared processor line
#print('%mem=3000mb')#memory line
#print('%chk=checkpoint_file.chk') #Checkpoint File)
print('#p opt pbe1pbe def2svp empiricaldispersion=gd3bj scf=xqc integral=(grid=ultrafine)\n') #Route card
print('Title Card Required\n') #Title Card
print('0 1') #Charge and Multiplicity
#Below are the xyz coordinates
for i in geometry:
    print(" {:<3}  {: .8f}  {: .8f}  {: .8f}".format(i[0], i[1], i[2], i[3]))
print('\n')
output_file.close()
#========================================================================================#
#------------------------------------------------------#
# To write the new coordinates into an ORCA input file #
#------------------------------------------------------#
#output_file2 = open(input('Enter the filename to write the new coordinates as ORCA input: ')+'.inp', "w")
output_file2 = open(pure_filename+'R'+'.inp', 'w')
sys.stdout = output_file2
print('%MaxCore 3000') # Amount of memory per core
print('% pal nprocs 16') #Number of Processors
print('    end') #End of Block
print('#Single Point Energy of test molecule') #Title Card
print('! PBE0 D3 RIJCOSX def2-SVP def2-SVP/J Grid5 GridX7 VERYTIGHTSCF\n') #Route Card
#print('! moread')
#print('%moinp "old_test.gbw"\n')
print('*xyz 0 1') #Charge and Multiplicity
#Below are the xyz coordinates
for i in geometry:
    print("{:<3}  {: .8f}  {: .8f}  {: .8f}".format(i[0], i[1], i[2], i[3]))
print('*')
output_file2.close()
#========================================================================================#
#-------------------------------------------------#
# To write the new coordinates into an xyz file   #
#-------------------------------------------------#
#output_file3 = open(input('Enter the filename to write the new coordinates as ORCA input: ')+'.inp', "w")
output_file3 = open(pure_filename+'R'+'.xyz', 'w')
sys.stdout = output_file3
print(n_atoms)
print('XYZ Coordinates of the given molecule')
#Below are the xyz coordinates
for i in geometry:
    print("{:<3}  {: .8f}  {: .8f}  {: .8f}".format(i[0], i[1], i[2], i[3]))

output_file3.close()
#========================================================================================#

#-----------------------------------#
# A Script by Muhammad Ali Hashmi   #
# muhammad.hashmi@vuw.ac.nz         #
#-----------------------------------#

