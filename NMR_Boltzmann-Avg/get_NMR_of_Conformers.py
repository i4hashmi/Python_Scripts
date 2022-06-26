from pylab import *
import glob
import os
import csv
import time

### Header
print("#======================================================================================================#")
print("#------------------------------------------------------------------------------------------------------#")
print("#                      A Script to Extract NMR values from Gaussian Output Files                       #")
print("#------------------------------------------------------------------------------------------------------#")
print("#======================================================================================================#")
print("\n")


###

# ----------------------------------------------------------------------------------------------------------------------------#
# A function to take out Atom No., Symbols, and NMR Shielding Tensor Values from a Gaussian log file and save them to lists  #
# ----------------------------------------------------------------------------------------------------------------------------#
# ---------- Start of Function ----------#
def NMR_shielding_tensors(input_file, Atom_No_List, Symbols_List, Tensors_List):
    atom_no = ""
    atom = ""
    shielding_tensor = ""
    f = open(input_file, 'r')
    input = f.readlines()
    filename = os.path.splitext(os.path.basename(input_file))[0]
    sublist_1 = []  # A list for Atom Numbers
    sublist_2 = []  # A list for Atom Symbols
    sublist_3 = [filename]  # A list for Gibbs Free Energy and Shielding tensors
    for line in reversed(
            input):  # Reading in reverse to find the triple zeta/last occuring Gibb' energy in case of multiple frequency calculations present in one file
        if "SCF Done" in line:
            complete_line = line  # Take the line containing SCF Done
            splitted_line = complete_line.split()  # Split the line with SCF Energy
            SCF_energy = float(splitted_line[4])  # Save the SCF Energy Value
            SCF_E_Kcal = float(SCF_energy) * 627.5095
            sublist_3.append(SCF_E_Kcal)
            # print("Here is the SCF Energy in Kcal/mol", SCF_E_Kcal)
            break
    for line in input:
        if "Isotropic =" in line:
            # print(line)
            complete_line = line.split()
            atom_no = complete_line[0]
            atom = complete_line[1]
            shielding_tensor = complete_line[4]
            sublist_1.append(int(atom_no))
            sublist_2.append(atom)
            sublist_3.append(float(shielding_tensor))
    Atom_No_List.append(sublist_1)  # Append atom numbers to the first list in argument
    Symbols_List.append(sublist_2)  # Append atom symbols to the second list in argument
    Tensors_List.append(sublist_3)  # Append the filename, SCF_Energy, and SHielding Tensors to the 3rd list in argument
    f.close()


# ---------- End of Function ----------#

# ----------------------- Definition of the lists to store the data -----------------------#
Atom_Numbers = []  # A list which will contain all the atom numbers in sequence
Atom_Symbols = []  # A list which will contain all the atom symbols for the atom numbers above
Shielding_Tensors = []  # A list which will contain all the shielding tensors for the atoms in above list

# ----------------------- Getting current directory and calling above function on all log files -----------------------#
directory = os.getcwd()  # A variable to get the path to current directory

for filename in os.listdir(directory):
    if filename.endswith(".log") or filename.endswith(".LOG"):
        NMR_shielding_tensors(filename, Atom_Numbers, Atom_Symbols, Shielding_Tensors)
        print(os.path.join(filename))
# --------------------------------------------------------------------------------------------------------------------#

# Take out Atom Numbers for First File only to Use them in CSV File
One_File_Atom_Nos = ["Atom_Numbers", " "]
for i in Atom_Numbers[0]:
    One_File_Atom_Nos.append(i)
# Take out Atom Symbols for First File only to Use them in CSV File
One_File_Atom_Symbols = ["Atom_Symbols", "SCF Energy"]
for i in Atom_Symbols[0]:
    One_File_Atom_Symbols.append(i)

# print("Atom Numbers", Atom_Numbers)
# print("Atom Symbols", Atom_Symbols)
# print("Shielding Tensors", Shielding_Tensors)
# --------------------------------------------------------------------------------------------------------------------#

# ------------------------------------------#
# A loop to write the output to a csv file  #
# ------------------------------------------#
with open('NMR_Results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL) # Defining general csv writing template
    writer.writerow(One_File_Atom_Nos)
    writer.writerow(One_File_Atom_Symbols)
    for i in Shielding_Tensors:
        writer.writerow(i)


print("\nAll Done, Check the output csv file for results.")
print('Processing Completed at : ', time.strftime("Time: %X, Date: %d/%m/%Y"), "\n")
print("#==============================================================#")
print("#=== A Script by Dr. Muhammad Ali Hashmi (October 06, 2021) ===#")
print("#==============================================================#")

# --------------------------------------------------------#
#  A Script by Dr. Muhammad Ali Hashmi (06-October-2021)  #
# --------------------------------------------------------#
