import os
import csv
import time
import math

# Constants
T = 298.15
R = 0.0083144626  # kJ/mol·K
RT = R * T  # ≈ 2.47895702419

# Header
print("#====================== NMR Shielding Tensor Processing Script =========================#")
print("#                Extracts NMR Shielding, Computes Boltzmann Averaged Values             #")
print("#========================================================================================#\n")


# Function to extract NMR data from Gaussian log file
def NMR_shielding_tensors(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    filename = os.path.splitext(os.path.basename(input_file))[0]
    atom_nos, symbols, tensors = [], [], []

    SCF_energy = None
    Gibbs_energy = None

    # Read energies from file
    for line in reversed(lines):
        if "Sum of electronic and thermal Free Energies" in line and Gibbs_energy is None:
            gibbs_line = line.split()
            Gibbs_energy = float(gibbs_line[7]) * 2625.5  # Convert Hartree to kJ/mol
        elif "SCF Done" in line and SCF_energy is None:
            SCF_energy = float(line.split()[4]) * 2625.5

        if Gibbs_energy and SCF_energy:
            break

    # Prefer Gibbs energy if available
    effective_energy = Gibbs_energy if Gibbs_energy is not None else SCF_energy

    # Read shielding tensors
    for line in lines:
        if "Isotropic =" in line:
            parts = line.split()
            atom_nos.append(int(parts[0]))
            symbols.append(parts[1])
            tensors.append(float(parts[4]))

    return {
        "filename": filename,
        "energy_kj": effective_energy,
        "gibbs_kj": Gibbs_energy,
        "scf_kj": SCF_energy,
        "atom_nos": atom_nos,
        "symbols": symbols,
        "tensors": tensors
    }


# Extract data from all .log files
conformer_data = []
for file in os.listdir():
    if file.endswith(".log") or file.endswith(".LOG"):
        data = NMR_shielding_tensors(file)
        conformer_data.append(data)
        print(f"Processed: {file}")

# Sort conformers by energy (lowest first)
conformer_data.sort(key=lambda x: x["energy_kj"])
min_energy = conformer_data[0]["energy_kj"]

# Compute Boltzmann factors and relative energies
partition_function = 0.0
for conf in conformer_data:
    rel_E = conf["energy_kj"] - min_energy
    conf["rel_energy"] = rel_E
    conf["boltzmann_factor"] = math.exp(-rel_E / RT)
    partition_function += conf["boltzmann_factor"]

# Normalize Boltzmann factors to get percentages
for conf in conformer_data:
    conf["boltzmann_percent"] = 100.0 * conf["boltzmann_factor"] / partition_function

# Boltzmann-averaged shielding tensors
num_atoms = len(conformer_data[0]["tensors"])
boltz_avg_tensors = [0.0 for _ in range(num_atoms)]
for conf in conformer_data:
    weight = conf["boltzmann_factor"] / partition_function
    for i in range(num_atoms):
        boltz_avg_tensors[i] += weight * conf["tensors"][i]

# Get atom numbers and symbols from first conformer
atom_numbers = conformer_data[0]["atom_nos"]
atom_symbols = conformer_data[0]["symbols"]

# CSV Output
with open('NMR_Boltzmann_Averaged.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Header
    header = [
        "Conformer", "SCF_Energy_kJ/mol", "Gibbs_Energy_kJ/mol",
        "Used_Energy_kJ/mol", "Relative_Energy_kJ/mol",
        "Boltzmann_Factor", "Boltzmann_%"
    ]
    header += [f"Atom_{i+1}" for i in range(num_atoms)]
    writer.writerow(header)

    # Data rows
    for conf in conformer_data:
        row = [
            conf["filename"],
            round(conf["scf_kj"], 4) if conf["scf_kj"] else "",
            round(conf["gibbs_kj"], 4) if conf["gibbs_kj"] else "",
            round(conf["energy_kj"], 4),
            round(conf["rel_energy"], 4),
            round(conf["boltzmann_factor"], 6),
            round(conf["boltzmann_percent"], 4)
        ]
        row += [round(t, 4) for t in conf["tensors"]]
        writer.writerow(row)

    # Extra spacing row
    writer.writerow([])

    # Atom number row
    atom_num_row = ["Atom_Numbers", "", "", "", "", "", ""] + atom_numbers
    writer.writerow(atom_num_row)

    # Atom symbol row
    atom_sym_row = ["Atom_Symbols", "", "", "", "", "", ""] + atom_symbols
    writer.writerow(atom_sym_row)

    # Boltzmann average row
    avg_row = ["Boltzmann_Averaged_Shielding_Tensors", "", "", "", "", "", ""]
    avg_row += [round(x, 4) for x in boltz_avg_tensors]
    writer.writerow(avg_row)

print("\n✅ All Done! Check 'NMR_Boltzmann_Averaged.csv' for results.")
print("📅 Completed at :", time.strftime("Time: %X, Date: %d/%m/%Y"))
