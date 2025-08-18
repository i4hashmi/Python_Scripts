Guidelines to use these scripts:

After running the CREST conformational analysis, you can use this script "crest_conf_separation.py" to separate the conformers in crest_ensemble.xyz file.
You can simply call it with "python3 crest_conf_separation.py crest_ensemble.xyz" and it will separate all the conformers and save their xyz files as conformer01.xyz, conformer02.xyz, etc.

Then you can use the other script to make Gaussian input files from these CREST conformers. That script can be used on one xyz file like:
python3 make_opt-freq-nmr_calc_from_Gaussian_output_files.py conformer01.xyz

OR if you want to run on all the xyz conformers, use with bash for loop as below:
for i in *.xyz; do python3 make_opt-freq-nmr_calc_from_Gaussian_output_files.py $i; done

It will generate Gaussian input files for all the conformers in the current directory.
