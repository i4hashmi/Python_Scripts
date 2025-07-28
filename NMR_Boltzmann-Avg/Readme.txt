This script reads all the NMR log files (from Gaussian software) and collects the MNR shielding tensors of all the molecules present in the current directory, gets SCF Energies/Gibbs Energies, then sorts them according to their relative energies (kJ/mol) and calculates their Boltzmann Percentage.
The script also produces a list of atoms and their Boltzmann-averaged NMR shielding tensors in a CSV file.
The usage of the script is simple. You just call it with Python, and it searches for all the log files in the present directory.
