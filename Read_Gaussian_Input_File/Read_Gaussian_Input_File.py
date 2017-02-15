import sys

print("#--------------------------------------------------------------------------------------------------#")
print("#--------------------------------------------------------------------------------------------------#")
print("# Script to Extract the XYZ Coordinates from a Gaussian Input File and Write them to Various Files #")
print("#--------------------------------------------------------------------------------------------------#")
print("#--------------------------------------------------------------------------------------------------#")

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

    print("Dated: February 15, 2017\n")


#############################################################################################################
# This section is for the definition of all the functions used by the script
#############################################################################################################
#========================================================================================#
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
        sys.stdout = open(self.filename+'R'+'.gjf', 'w')
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
        print('XYZ Coordinates of the given molecule')
        #Below are the xyz coordinates
        for i in geometry:
            print("{:<3}  {: .8f}  {: .8f}  {: .8f}".format(i[0], i[1], i[2], i[3]))
        sys.stdout.close()
        sys.stdout = output_file3
    #=====================================================#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% End of Class %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#

#-----------------------------------------------------------#
# Define a Function to Shorten a List from a Specific Index #
#-----------------------------------------------------------#
#-------------- Start of Function --------------#
def shorten(s, string_to_find):
    i = s.index(string_to_find)-1 # Find the index of the given string and exclude the string itself
    return s[:i+len(string_to_find)]
#--------------- End of Function ---------------#

#-----------------------------------------------#
# Define a Function to read the .gjf input File #
#-----------------------------------------------#
#-------------- Start of Function --------------#
def Read_gjf_File(input_file):
    f = open(input_file, 'r')
    fr = f.readlines()
    f.close()
    Lines_to_leave = 0
    # Check below the structure of input file and decide how many lines to leave before the coordinates
    if fr[0].startswith('%') and fr[1].startswith('%') and fr[2].startswith('%'):
        Lines_to_leave = 8
    elif fr[0].startswith('%') and fr[1].startswith('%') and fr[2].startswith('#'):
        Lines_to_leave = 7
    elif fr[0].startswith('%') and fr[1].startswith('#'):
        Lines_to_leave = 6
    elif fr[0].startswith('#'):
        Lines_to_leave = 5
    else:
        print('It does not seem a proper Gaussian input file')

    # Now start reading the coordinates
    f2 = open(input_file, 'r')
    read_coords = f2.readlines()[Lines_to_leave:] # A list with coordinates after the first lines including route line etc.
    f2.close()
    coords = shorten(read_coords, '\n') # List containing only the coordinates, deleting the geom = connectivity data
    geom = [] # Final Geometry of the molecule
    # A loop to save the extracted coordinates nicely in the list 'geom'
    for i in coords:
        sublist = []
        a = i.split()
        sublist.append(a[0])
        sublist.append(float(a[1]))
        sublist.append(float(a[2]))
        sublist.append(float(a[3]))
        geom.append(sublist)

    return geom
#--------------- End of Function ---------------#

#========================================================================================#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
###############################################################################
#                                                                             #
#                    The Main Part of the Program Starts Here                 #
#                                                                             #
###############################################################################
# Below is the input file which can be taken in the first argument and also as a file in the script
Input_File = sys.argv[1]
#Input_File = 'rimariki/rimarikiamide_test.gjf'

# Run the function on the input file and save the coordinates below
XYZ_Coordinates = Read_gjf_File(Input_File)

# Print the Coordinates below
#for i in XYZ_Coordinates:
#    print(" {:<3}  {: .8f}  {: .8f}  {: .8f}".format(i[0], i[1], i[2], i[3]))

# Write the output file
write_output = WriteOutputFile(XYZ_Coordinates, Input_File)
write_output.xyzFile(XYZ_Coordinates) # Write to an xyz file
#write_output.GaussianFile(XYZ_Coordinates) # Write to a Gaussian input file
#write_output.OrcaFile(XYZ_Coordinates) # Write to an ORCA input file
#========================================================================================#
# Developed by Muhammad Ali Hashmi (i4hashmi@hotmail.com)
Stamp_Hashmi()
#========================================================================================#
