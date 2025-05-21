import glob, os, csv

print("#=======================================================================================#")
print("#---------------------------------------------------------------------------------------#")
print("#              A Script to Extract SCF Energies, Elapsed Time, and Optical Rotation     #")
print("#---------------------------------------------------------------------------------------#")
print("#=======================================================================================#")
print("\n")

#---------- Start of Function ----------#
def SCF_Energy_and_Time(input_file):
    SCF_Energy = "--NOT FOUND--"
    SCF_E_kJ = "--NOT FOUND--"
    elapsed_time_hours = "--NOT FOUND--"
    opt_rot = "--NOT FOUND--"
    filename = os.path.splitext(os.path.basename(input_file))[0]

    with open(input_file, 'r') as f:
        input_lines = f.readlines()

    for line in input_lines:
        if "SCF Done:" in line:
            complete_line = line.split()
            SCF_Energy = complete_line[4]
            SCF_E_kJ = float(SCF_Energy) * 2625.50
        
        if "Elapsed time:" in line:
            parts = line.split()
            days = int(parts[2])
            hours = int(parts[4])
            minutes = int(parts[6])
            seconds = float(parts[8])
            # Convert total time to hours
            elapsed_time_hours = days * 24 + hours + minutes / 60 + seconds / 3600
        
        if "Molar Mass =" in line:
            # Assuming the optical rotation value appears after 'Alpha' symbol
            opt_rot = line.split("=")[-1].split("deg")[0].strip()

    return [filename, SCF_Energy, SCF_E_kJ, elapsed_time_hours, opt_rot]

# Define the list to hold all extracted data
Final_Energies_List = [['File Name', 'SCF Energy (a.u)', 'SCF Energy (kJ/mol)', 'Elapsed Time (hours)', 'Optical Rotation (deg)']]

# Process each log file in the directory
input_files = '*.log'
for file in glob.glob(input_files):
    Final_Energies_List.append(SCF_Energy_and_Time(file))

# Display results
print("Here are the SCF Energies, Elapsed Times, and Optical Rotations for all Files\n")
for i in Final_Energies_List:
    print("{:<10} {:<16} {:<20} {:<20} {:<20}".format(i[0], i[1], i[2], i[3], i[4]))

# Write results to CSV
with open('SCF_Energies_Time_OptRot.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(Final_Energies_List)
