This script can read a number of csv files (Filtered by a script of R) and specifically made for a specific type of data set. 
Two example files have been provided with the script. It can read the csv files, take the average of three retention times, select
the biggest value of area under the peak, and reproduce "Merged_Files" which have three columns, named: Chemical name, Average retention time,
and Maximum area.
After that it stores that data and makes a new list called "Chemical_Names" in which it stores all the names from all the input files. 
Here, it renames the duplicates with a "-Rep" at the end of chemical name. Then it reads through their average retention times and maximum area
to put in a final file with all the data arranged in it for comparison.
For any help contact at i4hashmi@hotmail.com

Usage on windows:
Just put the script in the folder containing "Filtered_csv_files" and double click(Run) it. It will create a new folder "Output" and put
the results in it.

Muhammad Ali Hashmi
