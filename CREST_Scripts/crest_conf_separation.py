
'''This script is to separate all the conformers from a CREST conformers scan file
This file is usually named crest_conformers.xyz and has all the conformers in it in
a sequence. The script can be used simply with python3 crest_conf_separation.py file.xyz'''

import sys
import re
import csv

def read_xyz_file(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    return data

def split_conformers(data):
    conformers = []
    i = 0
    while i < len(data):
        try:
            num_atoms = int(data[i].strip())
        except ValueError:
            print(f"Invalid number of atoms at line {i+1}.")
            break
        conformer_data = data[i:i + num_atoms + 2]
        conformers.append(conformer_data)
        i += num_atoms + 2
    return conformers

def extract_energy_from_comment_line(line):
    """Extracts first float found in the comment line (line 2 of xyz conformer)"""
    matches = re.findall(r"[-+]?\d*\.\d+|\d+", line)
    if matches:
        return float(matches[0])
    else:
        return None

def save_conformers_and_energies(conformers, energy_csv_filename):
    energies = []
    for index, conformer in enumerate(conformers):
        filename = f'conformer{index + 1:02}.xyz'
        with open(filename, 'w') as file:
            file.writelines(conformer)

        energy_line = conformer[1]  # Line 2 of each conformer block
        energy = extract_energy_from_comment_line(energy_line)
        energies.append((filename.replace('.xyz', ''), energy))  # <-- changed here

    # Write energies to CSV
    with open(energy_csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Energy (a.u.)"])
        writer.writerows(energies)

    print(f"All Done. Total conformers saved: {len(conformers)}")
    print(f"Energies saved in: {energy_csv_filename}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python merged_conf_energy.py <crest_conformers.xyz>")
        sys.exit(1)

    input_file = sys.argv[1]
    data = read_xyz_file(input_file)
    conformers = split_conformers(data)
    save_conformers_and_energies(conformers, "conformer_energies.csv")

if __name__ == "__main__":
    main()

