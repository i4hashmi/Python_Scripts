import sys # Import sys to write to output files

print("#----------------------------------------------------------------------------------------------#")
print("#----------------------------------------------------------------------------------------------#")
print("#         Script to Extract the Optimized Structure from a Gaussian or ORCA output File        #")
print("#----------------------------------------------------------------------------------------------#")
print("#----------------------------------------------------------------------------------------------#")


#############################################################################################################
# This section is for the definition of Dictionaries, Classes, Functions etc.
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
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+#
# A Class for Extracting the Optimized Coordinates from a Gaussian or ORCA ouput File#
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Start of Class %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
class ExtractCoords(object):
    """A Class for Extracting the Optimized Coordinates from a Gaussian or ORCA ouput File"""
    def __init__(self, file):
        self.file = file

    #------------------------------------------------------------------------------#
    # Define a function to read the input file and extract the optimized structure #
    #------------------------------------------------------------------------------#
    #----------------------------- Start of Function -----------------------------#
    def extractCoordinates(self, file):
        #print("\nExtracting the Molecule from the given output file")
        f = open(file, 'r')
        program = "N/A"
        # Determine if we're dealing with Gaussian16 or ORCA
        for line in f:
            if line.find("Entering Gaussian System, Link 0=g16") != -1 or line.find("Copyright (c) 1988-2019, Gaussian, Inc.  All Rights Reserved.") != -1:
                print("Reading Gaussian output file: ", file, '\n')
                program = "g16"
                break
            elif line.find("* O   R   C   A *") != -1:
                print("Reading ORCA output file: ", file, '\n')
                program = "orca"
                break
        f.close()

        # GEOMETRY READING SECTION
        geom = []
        # Read through Gaussian file, read "Standard orientation"
        if program == "g16":
            f = open(file, 'r')
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
            f = open(file, 'r')
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
    # ------------------------------------------------------------------------------#
    # Define a function to read the input file & extract the SCF energy of molecule #
    # ------------------------------------------------------------------------------#
    # ----------------------------- Start of Function -----------------------------#
    def extractEnergies(self, file):
        f = open(file, 'r')
        program = "N/A"
        # Determine if we're dealing with Gaussian16 or ORCA
        for line in f:
            if line.find("Entering Gaussian System, Link 0=g16") != -1 or line.find(
                    "Copyright (c) 1988-2019, Gaussian, Inc.  All Rights Reserved.") != -1:
                program = "g16"
                break
            elif line.find("* O   R   C   A *") != -1:
                program = "orca"
                break
        f.close()
        Charge = 0
        Multiplicity = 1
        SCF_Energy = "--SCF Energy NOT FOUND--"
        Zero_point_energy = "--ZPE NOT FOUND--"
        Gibbs_Energy = "--Delta-G NOT FOUND--"
        Rxn_Enthalpy = "--Enthalpy NOT FOUND--"
        SCF_E_Kcal = "--SCF_E_Kcal NOT FOUND--"
        Gibbs_E_Kcal = "--Gibbs_E_Kcal NOT FOUND--"
        Zero_point_energy_Kcal = "--ZPE_Kcal NOT FOUND--"
        Enthalpy_of_Rxn_Kcal = "--Enthalpy_Kcal NOT FOUND--"
        if program == "g16":
            f = open(file, 'r')
            input = f.readlines()
            #filename = os.path.splitext(os.path.basename(input_file))[0]
            for line in input:
                if "Charge =" in line:
                    complete_line = line.split()
                    #print("I found the charge as ",int(complete_line[2]))
                    Charge = int(complete_line[2])
                    Multiplicity = int(complete_line[5])
                if "SCF Done:" in line:
                    complete_line = line.split()
                    SCF_Energy = float(complete_line[4])
                    SCF_E_Kcal = float(SCF_Energy) * 627.5095
                if "Sum of electronic and zero-point Energies" in line:
                    complete_line = line.split()
                    Zero_point_energy = complete_line[6]
                    Zero_point_energy_Kcal = float(Zero_point_energy) * 627.5095
                if "Sum of electronic and thermal Free Energies" in line:
                    gibbs_line = line.split()
                    Gibbs_Energy = gibbs_line[7]
                    Gibbs_E_Kcal = float(Gibbs_Energy) * 627.5095
                if "Sum of electronic and thermal Enthalpies" in line:
                    enthalpies_line = line.split()
                    Rxn_Enthalpy = enthalpies_line[6]
                    Enthalpy_of_Rxn_Kcal = float(Rxn_Enthalpy) * 627.5095
            return [Charge, Multiplicity, SCF_Energy, SCF_E_Kcal, Zero_point_energy, Zero_point_energy_Kcal, Gibbs_Energy,
                    Gibbs_E_Kcal, Rxn_Enthalpy, Enthalpy_of_Rxn_Kcal]
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% End of Class %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+#
#               A Class for Writing the Script Output to an output file              #
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Start of Class %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
class WriteOutputFile(object):
    """A Class for Writing the Script Output to an output file for Gaussian, ORCA, or an xyz file"""
    def __init__(self, geometry, filename):
        self.geometry = geometry
        #self.filename = filename
        self.filename = filename.split('\\').pop().split('/').pop().rsplit('.', 1)[0]

    #----------------------------------------------------#
    # To write the new coordinates into a Gaussian file  #
    #----------------------------------------------------#
    def GaussianFile(self, geometry):
        output_file = sys.stdout
        sys.stdout = open(self.filename+suffix_filename+'.com', 'w')
        #print('%nprocshared=24') #shared processor line
        #print('%mem=3000mb')#memory line
        print('%chk='+self.filename+suffix_filename+'.chk') #Checkpoint File)
        print(Route_Card_Gaussian+'\n') #Route card
        print('Frequency of the Optimized Molecule\n') #Title Card
        print(Charge, Multiplicity) #Charge and Multiplicity
        #Below are the xyz coordinates
        for i in geometry:
            print(" {:<3}  {: .8f}  {: .8f}  {: .8f}".format(i[0], i[1], i[2], i[3]))
        #print('\n'+Gen_Basis)  ## Uncomment this to print the basis set info at the end of file
        #print('\n' + Solvation_gen)  ## Uncomment this to print the Generic Solvent at the end of file
        print('\n')
        sys.stdout.close()
        sys.stdout = output_file
    #=====================================================#
    #------------------------------------------------------#
    # To write the new coordinates into an ORCA input file #
    #------------------------------------------------------#
    def OrcaFile(self, geometry):
        output_file2 = sys.stdout
        sys.stdout = open(self.filename+'R'+'.inp', 'w')
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
        sys.stdout.close()
        sys.stdout = output_file2
    #=====================================================#

    #-------------------------------------------------#
    # To write the new coordinates into an xyz file   #
    #-------------------------------------------------#
    def xyzFile(self, geometry):
        # Find the total number of atoms in the molecule
        n_atoms = len(geometry)
        output_file3 = sys.stdout
        sys.stdout = open(self.filename+'.xyz', 'w')
        print(n_atoms)
        print('Charge = ', Charge, 'Multiplicity =', Multiplicity, 'SCF Energy = ', SCF_energy, 'au')
        #Below are the xyz coordinates
        for i in geometry:
            print("{:<3}  {: .8f}  {: .8f}  {: .8f}".format(i[0], i[1], i[2], i[3]))
        sys.stdout.close()
        sys.stdout = output_file3
    #=====================================================#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% End of Class %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#

#==============================================================================#

###############################################################################
#                                                                             #
#                    The Main Part of the Program Starts Here                 #
#                                                                             #
###############################################################################

# Specify the output file
# Take the input file in the first argument. Uncomment below if you want to use the script in linux with file in the first argument
output_file = sys.argv[1]
#output_file = 'imidazolium.log'
#output_file = 'sulphate.log'

# Molecule is a variable that runs the class ExtractCoords
molecule = ExtractCoords(output_file)
all_energies = molecule.extractEnergies(output_file) # This list contains all the energies extracted above
SCF_energy = all_energies[2]
Charge = all_energies[0]
Multiplicity = all_energies[1]
##################################################################################
################# Below Data is to be Changed as per Requirement #################
##################################################################################
suffix_filename = '1'
Route_Card_Gaussian = '#p freq=raman b3lyp/6-311+g(d,p) empiricaldispersion=gd3bj int=ultrafine scf=conver=9'
Gen_Basis = """\
C H N Cl 0
6-31G(d,p)
****
I 0
LanL2DZ
****

I 0
LanL2DZ"""
Solvation_gen='eps=11.4 epsinf=1.40 HBondAcidity=0.0 HBondBasicity=0.0 SurfaceTensionAtInterface=70.24 CarbonAromaticity=0.1765 ElectronegativeHalogenicity=0.3529'
#print("Here is the SCF Energy",SCF_energy)
#print("Charge on the molecule is: ", Charge)
#print("Multiplicity on the molecule is: ", Multiplicity)

# Define a list to store the extracted structure from the output file
geometry = molecule.extractCoordinates(output_file)
# Print the extracted coordinates
#print('The total number of atoms in the given molecule are:', n_atoms, '\n')
#for i in geometry:
#    print("{:<3}  {: .8f}  {: .8f}  {: .8f}".format(i[0], i[1], i[2], i[3]))

#========================================================================================#
write_output = WriteOutputFile(geometry, output_file) # Class to write the extracted geometry to a file
#write_output.GaussianFile(geometry) # Write to a Gaussian input file
#write_output.OrcaFile(geometry) # Write to an ORCA input file
write_output.xyzFile(geometry) # Write to an xyz file

#========================================================================================#
#Stamp_Hashmi()
#-----------------------------------#
# A Script by Muhammad Ali Hashmi   #
# compchem394@gmail.com             #
#-----------------------------------#

