import glob
import csv
import numpy
import os

# Copyright Muhammad Ali Hashmi. You may use this script, do changes, and reproduce it. Please be brave enough to acknowledge the original author. Cheers

print("#======================================================================================================#")
print("#------------------------------------------------------------------------------------------------------#")
print("#                      A Script by Hashmi to Work with Dr. AlZeer's Crazy Research                     #")
print("#------------------------------------------------------------------------------------------------------#")
print("#======================================================================================================#")
print("\n")

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=#
#   A Class for Reading a CSV File, Sorting Data, and Writing the Output to a CSV File    #
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Start of Class %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
class ExtractData(object):
    """A Class to read the given csv file and extract the selected data out of it to do different operations and save it as another csv file"""
    def __init__(self, file):
        self.file = file
        self.filename = file.split('\\').pop().split('/').pop().rsplit('.', 1)[0]

    #-------------------------------------------------------------------------------------------------------------------#
    # Define a Function to read the csv File and take out the columns of your interest along with finding average etc.  #
    #-------------------------------------------------------------------------------------------------------------------#
    #-------------- Start of Function --------------#
    def Read_csv(self, file):
        csvfile = open(file, 'r')
        csvreader = csv.reader(csvfile, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True) #Read the csv file with using commas and quotes as delimiters
        next(csvreader) # Remove the firs line of the csv file
        kept_values = []#['Chemical Name', 'Average Ret. Time', 'Maximum Area']]
        for row in csvreader:
            sublist = []
            sublist.append(row[0])
            retention_times = [float(row[1]) if row[1] != 'NA' else 0, float(row[9]) if row[9] != 'NA' else 0, float(row[17]) if row[17] != 'NA' else 0]
            new_ret_times = [value for value in retention_times if value != 0] # Tom remove the zeroes due to 'NA'
            #Avg_ret_time = numpy.mean(retention_times)
            Avg_ret_time = numpy.mean(new_ret_times)
            sublist.append(Avg_ret_time)
            areas = [float(row[2]) if row[2] != 'NA' else 0, float(row[10]) if row[10] != 'NA' else 0, float(row[18]) if row[18] != 'NA' else 0]
            sublist.append(max(areas))
            kept_values.append(sublist)

        return kept_values
    #--------------- End of Function ---------------#

    #----------------------------------------------------------#
    # Define a Function to Write the contents into a csv File  #
    #----------------------------------------------------------#
    #-------------- Start of Function --------------#
    def Write_csv(self, list_of_lists):
        output_file = open('Output/Merged_'+self.filename+'.csv', 'w')
        writer = csv.writer(output_file, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True) # Defining general csv writing template
        for i in list_of_lists:
            writer.writerow(i)
    #--------------- End of Function ---------------#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% End of Class %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#


###############################################################################
#                                                                             #
#                    The Main Part of the Program Starts Here                 #
#                                                                             #
###############################################################################

# Check if the directory for output exists and create if not
if not os.path.exists('Output'):
    os.makedirs('Output')

# Below variable is to contain all the csv files in the directory specified
All_Files = glob.glob('*.csv')
All_Filenames = []
All_Data = []

# Run the Class and Function to get all the data organized
#-------------------- Start of Loop --------------------#
for file in All_Files:
    ReadFile = ExtractData(file)
    Data1 = ReadFile.Read_csv(file)
    Data1.sort(key=lambda tup: tup[0]) # Sort the data alphabetically
    #Data1.insert(0, ['Chemical Name', 'Average Ret. Time', 'Maximum Area']) # Insert the titles at the begining of the list
    #print(Data1)
    All_Data.append(Data1)
    All_Filenames.append(ReadFile.filename)
    ReadFile.Write_csv(Data1) # If you do not want the Merged Files, comment this line
#--------------------- End of Loop ---------------------#

# Below I am comparing all the chemical names and change them to name1, name2, etc. for duplicate ones
#---------------------------------- Start of Loop ----------------------------------#
for sublist1 in All_Data:
    for sublist2 in range(len(sublist1)):
        for sublist3 in range(sublist2+1, len(sublist1)):
            if sublist1[sublist2][0] == sublist1[sublist3][0]:
                sublist1[sublist3][0] = sublist1[sublist3][0]+'-Rep'
                #print(sublist1[sublist2][0], '==', sublist1[sublist3][0])
#----------------------------------- End of Loop -----------------------------------#

# Below list is for all the chemical names with duplicates renamed
Chemical_Names = []
#---------------------------------- Start of Loop ----------------------------------#
for items in All_Data:
    for chemical in items:
        Chemical_Names.append(chemical[0]) if chemical[0] not in Chemical_Names else None

Chemical_Names.sort()
#----------------------------------- End of Loop -----------------------------------#

# Below List Contains All the Final Data, All Chemical_Names, Average Ret. Times, and Maximum_Area
Final_List_of_all_Samples = [['Chemical Names']]

# Below Loop is to make a list for the Header of the final file showing the names of the species
#---------- Start of Loop ----------#
for a in Final_List_of_all_Samples:
    for b in All_Filenames:
        a.append(b)
        a.append(b)
#----------- End of Loop -----------#

print('Here are the Chemical Names:', Chemical_Names)
#print(All_Data)
for i in All_Data:
    print(i)
# A loop to go through the lists "Chemical_Names" and "All_Data" and match the contents and make the final list
#-------------- Start of Loop --------------------#
for c in Chemical_Names:
    sublist4 = []
    sublist4.append(c)
    for d in All_Data:
        for e in d:
            if c == e[0]:
                sublist4.append(e[1])
                sublist4.append(e[2])
                break
        if c not in e:
            sublist4.append('')
            sublist4.append('')
    print(sublist4)
    Final_List_of_all_Samples.append(sublist4)
#--------------- End of Loop ---------------------#
#--------------------------------------------------------------------------------------------------------------------------------------------------#
# Write the Chemical Names to a CSV File
output_file2 = open('Output/All_Data_Sorted_دکتور.csv', 'w', newline='')
writer = csv.writer(output_file2, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True) # Defining general csv writing template
for name in Final_List_of_all_Samples:
    writer.writerow(name)
#--------------------------------------------------------------------------------------------------------------------------------------------------#

print('All Done Boss!\n')
print("#========================================================#")
print("#=== A Script by Muhammad Ali Hashmi (April 15, 2017) ===#")
print("#========================================================#")

