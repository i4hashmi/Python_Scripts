import os
import csv
import time
import math
from collections import Counter

# Constants
T = 298.15
R = 0.0083144626  # kJ/mol·K
RT = R * T  # ≈ 2.47895702419

# Header
print("#====================== NMR Shielding Tensor Processing Script =========================#")
print("#        Extracts energies/tensors, computes Boltzmann (consistent energy basis)        #")
print("#========================================================================================#\n")


# Function to extract NMR data from Gaussian log file
def NMR_shielding_tensors(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    filename = os.path.splitext(os.path.basename(input_file))[0]
    atom_nos, symbols, tensors = [], [], []

    scf_kj = None
    gibbs_kj = None

    # Read energies (reverse to get latest)
    for line in reversed(lines):
        if ("Sum of electronic and thermal Free Energies" in line) and (gibbs_kj is None):
            parts = line.split()
            gibbs_kj = float(parts[7]) * 2625.5  # Hartree -> kJ/mol
        elif ("SCF Done" in line) and (scf_kj is None):
            parts = line.split()
            scf_kj = float(parts[4]) * 2625.5
        if gibbs_kj is not None and scf_kj is not None:
            break

    # Read shielding tensors
    for line in lines:
        if "Isotropic =" in line:
            parts = line.split()
            atom_nos.append(int(parts[0]))
            symbols.append(parts[1])
            tensors.append(float(parts[4]))

    return {
        "filename": filename,
        "gibbs_kj": gibbs_kj,
        "scf_kj": scf_kj,
        # energy_kj will be set later based on global energy_mode
        "energy_kj": None,
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
        if len(data["tensors"]) == 0:
            print(f"⚠️  {file}: No NMR shielding tensors found. It will be EXCLUDED from Boltzmann calculations (kept in CSV).")
        else:
            print(f"Processed tensors: {file}")

if len(conformer_data) == 0:
    print("❌ No .log files found in the current directory.")
    raise SystemExit(1)

# Decide energy basis: ONLY use Gibbs if EVERY conformer has it; otherwise use SCF for ALL
all_have_gibbs = all(c["gibbs_kj"] is not None for c in conformer_data)
energy_mode = "gibbs" if all_have_gibbs else "scf"

if energy_mode == "gibbs":
    print("\n✅ Using Gibbs Free Energies for ALL conformers (all files had Gibbs).")
else:
    print("\nℹ️  Not all conformers had Gibbs Free Energy; using SCF energies for ALL conformers to keep the basis consistent.")

# Set the energy used according to chosen basis
for c in conformer_data:
    c["energy_kj"] = c["gibbs_kj"] if energy_mode == "gibbs" else c["scf_kj"]

# Safety: ensure we have energies for sorting; if any file lacks even SCF, warn
missing_energy = [c["filename"] for c in conformer_data if c["energy_kj"] is None]
if missing_energy:
    print("⚠️  These files had no usable energy (SCF/Gibbs not found) and will be placed last in the CSV:", ", ".join(missing_energy))

# Sort by used energy, placing missing at end
conformer_data.sort(key=lambda x: (x["energy_kj"] is None, x["energy_kj"] if x["energy_kj"] is not None else float('inf')))

# Build list of "valid" conformers for Boltzmann: must have tensors and matching atom count
nonempty = [c for c in conformer_data if len(c["tensors"]) > 0]

if len(nonempty) == 0:
    print("\n❗ No conformers with shielding tensors found. Will write energies only; no Boltzmann averages possible.")
    num_atoms = 0
    valid_conformers = []
else:
    # Choose the most common tensor length to avoid mismatches silently breaking averages
    length_counts = Counter(len(c["tensors"]) for c in nonempty)
    target_num_atoms, _ = max(length_counts.items(), key=lambda kv: kv[1])
    # Anything not matching target count is excluded (warn)
    valid_conformers = []
    for c in nonempty:
        if len(c["tensors"]) == target_num_atoms:
            valid_conformers.append(c)
        else:
            print(f"⚠️  {c['filename']}: Tensor length {len(c['tensors'])} differs from majority ({target_num_atoms}). Excluding from Boltzmann calc (kept in CSV).")
    num_atoms = target_num_atoms if valid_conformers else 0

# Compute Boltzmann only over valid_conformers
partition_function = 0.0
min_energy = None
if valid_conformers:
    # Min energy among valid set (basis: selected energy_mode)
    min_energy = min(c["energy_kj"] for c in valid_conformers if c["energy_kj"] is not None)

    # Compute factors
    for c in valid_conformers:
        rel_E = c["energy_kj"] - min_energy
        c["rel_energy"] = rel_E
        c["boltzmann_factor"] = math.exp(-rel_E / RT)
        partition_function += c["boltzmann_factor"]

    # Compute percentages
    for c in valid_conformers:
        c["boltzmann_percent"] = 100.0 * c["boltzmann_factor"] / partition_function if partition_function > 0 else None

    # Boltzmann-averaged shielding tensors
    boltz_avg_tensors = [0.0 for _ in range(num_atoms)]
    for c in valid_conformers:
        weight = c["boltzmann_factor"] / partition_function if partition_function > 0 else 0.0
        for i in range(num_atoms):
            boltz_avg_tensors[i] += weight * c["tensors"][i]
else:
    boltz_avg_tensors = []

# For conformers excluded from Boltzmann (no tensors or mismatched), still compute/display relative energy
# relative to min_energy of valid set (if available)
for c in conformer_data:
    if min_energy is not None and c["energy_kj"] is not None:
        c["rel_energy"] = c["energy_kj"] - min_energy
    else:
        c["rel_energy"] = None

    # Fill Boltzmann fields only for the valid set
    if c in valid_conformers:
        # already set above
        pass
    else:
        c["boltzmann_factor"] = None
        c["boltzmann_percent"] = None

# Get atom numbers and symbols from first valid conformer (if any)
atom_numbers = valid_conformers[0]["atom_nos"] if valid_conformers else []
atom_symbols = valid_conformers[0]["symbols"] if valid_conformers else []

# CSV Output
out_name = 'NMR_Boltzmann_Averaged.csv'
with open(out_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Header
    header = [
        "Conformer",
        "SCF_Energy_kJ/mol",
        "Gibbs_Energy_kJ/mol",
        "Used_Energy_kJ/mol",
        "Relative_Energy_kJ/mol",
        "Boltzmann_Factor",
        "Boltzmann_%"
    ]
    header += [f"Atom_{i+1}" for i in range(num_atoms)]
    writer.writerow(header)

    # Data rows
    for c in conformer_data:
        row = [
            c["filename"],
            round(c["scf_kj"], 6) if c["scf_kj"] is not None else "",
            round(c["gibbs_kj"], 6) if c["gibbs_kj"] is not None else "",
            round(c["energy_kj"], 6) if c["energy_kj"] is not None else "",
            round(c["rel_energy"], 6) if c["rel_energy"] is not None else "",
            (f"{c['boltzmann_factor']:.6f}" if c["boltzmann_factor"] is not None else ""),
            (f"{c['boltzmann_percent']:.4f}" if c["boltzmann_percent"] is not None else "")
        ]
        # Only print tensors if the row has the expected count
        if num_atoms and len(c["tensors"]) == num_atoms:
            row += [round(t, 6) for t in c["tensors"]]
        writer.writerow(row)

    # Extra spacing row
    writer.writerow([])

    # If we have valid conformers (and thus atom metadata), write the two helper rows and the average
    if valid_conformers:
        # Atom number row
        atom_num_row = ["Atom_Numbers", "", "", "", "", "", ""] + atom_numbers
        writer.writerow(atom_num_row)

        # Atom symbol row
        atom_sym_row = ["Atom_Symbols", "", "", "", "", "", ""] + atom_symbols
        writer.writerow(atom_sym_row)

        # Boltzmann average row
        avg_row = ["Boltzmann_Averaged_Shielding_Tensors", "", "", "", "", "", ""]
        avg_row += [round(x, 6) for x in boltz_avg_tensors]
        writer.writerow(avg_row)
    else:
        writer.writerow(["(No valid NMR tensors found among conformers — averages not computed)"])

print(f"\n✅ All Done Boss!!! I Wrote: {out_name} file for your consideration.")
print("📅 Completed at :", time.strftime("Time: %X, Date: %d/%m/%Y"))
