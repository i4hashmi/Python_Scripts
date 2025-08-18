import sys
import re

print("#----------------------------------------------------------#")
print("# Script to Create a Gaussian Input File from an XYZ File  #")
print("#----------------------------------------------------------#")

class ExtractCoords:
    """Class for Extracting Coordinates from an XYZ File"""
    def __init__(self, file):
        self.file = file

    def extractCoordinates(self):
        with open(self.file, 'r') as xyz_file:
            lines = xyz_file.readlines()

        n_atoms = int(lines[0].strip())  # First line: number of atoms
        title = lines[1].strip()         # Second line: title or comment

        geometry = []
        unique_elements = set()

        for line in lines[2:2 + n_atoms]:
            parts = line.split()
            if len(parts) == 4:
                element, x, y, z = parts[0], float(parts[1]), float(parts[2]), float(parts[3])
                geometry.append([element, x, y, z])
                unique_elements.add(element)
            else:
                print(f"Line skipped (not in format): {line.strip()}")

        charge = 0
        multiplicity = 1

        return charge, multiplicity, geometry, unique_elements


class WriteOutputFile:
    """Class for Writing the Geometry to a Gaussian Input File"""
    def __init__(self, charge, multiplicity, geometry, filename, prefix="", suffix=""):
        self.charge = charge
        self.multiplicity = multiplicity
        self.geometry = geometry
        base_filename = filename.split('\\').pop().split('/').pop().rsplit('.', 1)[0]
        self.output_filename = f"{prefix}{base_filename}{suffix}"
    
    def write_gaussian_file(self, geometry):
        output_file = sys.stdout
        sys.stdout = open(f"{self.output_filename}.com", "w")

        print(f"%chk={self.output_filename}.chk")
        print(Route_Card_Opt + '\n')
        print("Optimization of the Molecule in Gas Phase\n")
        print(self.charge, self.multiplicity)
        for atom in geometry:
            print(f" {atom[0]:<3}  {atom[1]: .8f}  {atom[2]: .8f}  {atom[3]: .8f}")
        print(Gen_Basis_LAN_Opt)

        print("--Link1--")
        print(f"%chk={self.output_filename}.chk")
        print(Route_Card_OR + '\n')
        print("Optical Rotation of the Optimized Molecule in Solvent\n")
        print(self.charge, self.multiplicity)
        print("\n589nm")
        print(Gen_Basis_LAN_NMR)

        print("--Link1--")
        print(f"%chk={self.output_filename}.chk")
        print(Route_Card_NMR + '\n')
        print("NMR of the Optimized Molecule in Solvent\n")
        print(self.charge, self.multiplicity)
        print(Gen_Basis_LAN_NMR)
        print('\n')

        sys.stdout.close()
        sys.stdout = output_file


###############################################################################
#                     Main Program Starts Here                                # 
###############################################################################
if len(sys.argv) < 2:
    print("Usage: python script.py <xyz_file> [prefix] [suffix]")
    sys.exit(1)

### Here, if you give the prefix and suffix after filename, it will add them to filename, otherwise it will keep the original filename
xyz_file = sys.argv[1]
prefix_filename = sys.argv[2] if len(sys.argv) > 2 else ""
suffix_filename = sys.argv[3] if len(sys.argv) > 3 else ""

### Extract xyz coordinates from xyz file
molecule = ExtractCoords(xyz_file)
charge, multiplicity, geometry, unique_elements = molecule.extractCoordinates()

#####################################################################################################################
### Below are the rout cards for optimization, optical rotation, and NMR. You can change them according to your needs
Route_Card_Opt = '# opt=tight b3lyp/gen empiricaldispersion=gd3bj int=ultrafine scf=conver=9 pseudo=cards'
Route_Card_OR = '# polar=optrot cphf=rdfreq b3lyp/gen empiricaldispersion=gd3bj int=ultrafine scf=conver=9 scrf=(solvent=chloroform) pseudo=cards geom=check guess=read'
Route_Card_NMR = '# nmr=giao mpw1pw91/gen int=ultrafine scf=conver=9 pseudo=cards scrf=(solvent=chloroform) geom=check guess=read'

Gen_Basis_LAN_Opt = f"""
{' '.join(element for element in unique_elements if element != 'I')} 0
6-31+G(d,p)
****
"""
if 'I' in unique_elements:
    Gen_Basis_LAN_Opt += """\
I 0
LanL2DZ
****

I 0
LanL2DZ
"""

Gen_Basis_LAN_NMR = f"""
{' '.join(element for element in unique_elements if element != 'I')} 0
6-311+G(2d,p)
****
"""
if 'I' in unique_elements:
    Gen_Basis_LAN_NMR += """\
I 0
LanL2DZ
****

I 0
LanL2DZ
"""

Iodine_radius = 'I 2.74'
Solvation_gen = 'eps=13.7 epsinf=1.54 HBondAcidity=0.18 HBondBasicity=0.52 SurfaceTensionAtInterface=68.29 CarbonAromaticity=0.231 ElectronegativeHalogenicity=0.0'
#####################################################################################################################

write_output = WriteOutputFile(charge, multiplicity, geometry, xyz_file, prefix_filename, suffix_filename)
write_output.write_gaussian_file(geometry)

print("#------------------------------------------------------------------------------#")
print(f"# All Done Boss! The file {write_output.output_filename}.com has been written  ")
print("#------------------------------------------------------------------------------#")

### A script by Muhammad Ali Hashmi (14 August 2025)