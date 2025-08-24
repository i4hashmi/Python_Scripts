Guidelines to use these scripts:
A complete video guideline is available at this playlist that is in line with all these scripts. Watch it to master this process:
https://www.youtube.com/playlist?list=PLWk-zl-RHnbeYi6NB5Yy_o7EY2JEiXyVf


After running the CREST conformational analysis, you can use this script "crest_conf_separation.py" to separate the conformers in crest_ensemble.xyz file.
You can simply call it with "python3 crest_conf_separation.py crest_ensemble.xyz" and it will separate all the conformers and save their xyz files as conformer01.xyz, conformer02.xyz, etc.

Then you can use the other script to make Gaussian input files from these CREST conformers. That script can be used on one xyz file like:
python3 make_opt-freq-nmr_calc_from_Gaussian_output_files.py conformer01.xyz

OR if you want to run on all the xyz conformers, use with bash for loop as below:
for i in *.xyz; do python3 make_opt-freq-nmr_calc_from_Gaussian_output_files.py $i; done

It will generate Gaussian input files for all the conformers in the current directory.

After that, you run all the calculations using Gaussian and get all the output files in the same directory. Then you can run the script 'get_SCF_energies.py' to get the SCF energies and optical rotation values of the conformers. These can be put in Comp-01_conformers_energies_OR_etc.xlsx file and then you can remove the duplicates as I told in the video.
Then you can run the script 'boltzmann_NMR_of_conformers.py' on all the unique conformers to get the NMR data and do the rest of the analysis in Excel sheet 'Comp-01_NMR_CHESHIRE_EXAMPLE.xlsx' as described in the final two videos.
This will give you the overall NMR data comparison.
