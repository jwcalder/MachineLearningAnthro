# Preprocessing raw data into machine learning datasets

This folder contains the code for preprocessing the raw data we collected and converting it into break-level and fragment-level datasets that can be used in machine learning. An overview of the scripts and the order in which to run them is below. The scripts generate the files `break_level_ml.csv` and `frag_level_ml.csv`, which are used as input the the machine learning algorithms and can also be found in the data folder in the parent directory.

The raw data is contained in the pp files in the main github directory, and the csv files `finaldata_angle_level.csv`, `mesh_stats.csv`, `finaldata_inventoryall.csv`, `finaldata_trabecula.csv`, and `manaul_break_level.csv`. All other csv files are generated by the preprocessing.

1. `process_ppfiles.py`: This script loads the pp files from meshlab and generates `break_ep_data.csv`. The ppfiles are located in the ppfiles folder in the parent directory.
2. `process_VG_data.py`: This script takes as input a csv file generated by the virtual goniometer (VG), and transforms the data into a 2D python dictionary that allows easy access to the VG information by fragment name, and break number. The script saves the dictionary in the pkl file `break_curve_data.pkl` which can be used by other scripts.  This script requires `finaldata_angle_level.csv` and the file `break_ep_data.csv` generated in Step 1. 
3. `mesh_stats.py`: This script computes statistics of each mesh directly from the 3D models and stores them in the file `mesh_stats.csv`. This script requires access to the raw meshes in the `finaldata_VtgonMeshes` folder (to be provided in github at a later date).
4. `frag_data.py`: This script compiles the fragment level data, from both `mesh_stats.csv`, the inventory file `finaldata_inventoryall.csv`, and the trabeculae file `finaldata_trabecula.csv`. This generates `frag_data.csv`. 
5. `compile_break_level_ml.py`: This generates the dataset to be used for machine learning at the break level. It requires `manaul_break_level.csv`, `mesh_stats.csv`, and `break_curve_data.pkl`. The script outputs the dataset to the file `break_level_ml.csv`.
6. `compile_frag_level_ml.py`: This generates the dataset to be used for machine learning at the fragment level. It requires `break_level_ml.csv` and `frag_data.csv`, and outputs the dataset to `frag_level_ml.csv`.


