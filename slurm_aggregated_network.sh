#!/bin/bash

#SBATCH --job-name=GITHUB_agg_root
#SBATCH --output=res_root_TOP420_%j.txt
#SBATCH --partition=long
#SBATCH --time=5-23:00:00
#SBATCH --ntasks=1 
#SBATCH --cpus-per-task=35
#SBATCH --mem=500gb

module load python/3.8
module load R/4.2.1

# Choose from the following tissues (leaf, fruit, seedless_fruit, root, stem, wood, flower, seed, tendril, bud, mix) and list them separated by a semicolon (e.j. leaf;berry will do the network of both leaf and berry tissues combined). For doing the independent network, tissue='ALL'.
# Remember to change job-name and output with the tissue

#PARAMETERS TO EDIT

metadata_file='/storage/TOM/SRA_vitis/metadata/final_classification.csv'
count_summaries_folder='/storage/TOM/SRA_vitis/count_summaries/'
count_matrices_folder='/storage/TOM/SRA_vitis/count_matrices/'
tissue='root'
result_folder='/storage/TOM/SRA_vitis/network/agg_root'
scripts='/storage/TOM/SRA_vitis/scripts/GITHUB_agg_network_pipeline'
anno='/storage/TOM/SRA_vitis/scripts/GITHUB_agg_network_pipeline/annotations.rda'

# DO NOT TOUCH ANYTHING BELOW THIS LINE

cd $scripts

echo 
echo '**************** PREPARING RAW COUNTS MATRIX ****************'
echo 

# The "preparing_experiments_folders.py" script selects all the runs in SRA that come from the selected tissue/s, copy then in the base folder, removes the runs with less than 10 M alignments, separate the runs in their respective experiment folders and finally removes the experiments with less than 4 runs.

base=$result_folder
PCC=$base'/PCCs'
HRR=$base'/binary_HRR_matrix_TOP420'
co_ocurrence=$base'/co_ocurrence'

mkdir -p $base

python3 preparing_experiments_folders.py --tissues_list $tissue --network_folder $base --metadata_file $metadata_file --count_summaries_folder $count_summaries_folder --count_matrices_folder $count_matrices_folder

# The "loop_merge_matrix.py" script iterates the experiment folders and generates a raw count matrix for experiment. This new raw count matrix (referred from now on as "all_counts" matrix) contains the counts of every run of the experiment.

python3 loop_merge_matrix.py -r $base -s $scripts

echo 
echo '**************** COMPUTING PCC MATRIX FOR EVERY EXPERIMENT ****************'
echo 

# The "loop_PCC.py" script computes the PCC matrix for each experiment. Briefly, for each experiment it reads the "all_counts" matrix, does a FPKM normalization and filters out the genes that in all the samples FPKM < 0.5. After that, with the remaining genes, it computes the PCC for the experiment.

python3 loop_PCC.py -p $base -s $scripts -a $anno

cd $base
mkdir $PCC
mv *PCC.txt* PCCs
cd $scripts

echo 
echo '**************** COMPUTING HRR MATRIX FOR EVERY EXPERIMENT ****************'
echo 

# Generating the HRR matrix from each PCC matrix with the "loop_HRR_generation_TOP420.py" script. This script will analyze each PCC matrix in order to generate its corresponding HRR matrix.

python3 -u loop_HRR_generation_TOP420.py -p $PCC -s $scripts

cd $base
mkdir $HRR
cd $PCC
mv *binary_HRR_matrix.csv $HRR
cd $scripts

mkdir $co_ocurrence

echo
echo '**************** COMPUTING CO-OCCURRENCE ACROSS EXPERIMENTS ****************'
echo

# Computing the co-ocurrence matrix with "concurrencia_data.table.R" Rscript. This script will analyze all the HRR matrix previously generated.

Rscript concurrencia_data.table.R $HRR'/' $co_ocurrence/co_occurrence_table.csv

sed -e 's/V1\t/\t/g' $co_ocurrence/co_occurrence_table.csv > $co_ocurrence/co_occurrence_table_def.csv

echo
echo '**************** FORMATING, FILTERING AND EVALUATING THE CO-OCCURRENCE MATRIX ****************'
echo

# The "top1_co_occurrence_matrix_version2_TOP420.py" script will filter the co-occurrence matrix, keeping only the TOP 420 co-expressed genes for each row of the non-filtered co-occurrence matrix. This script will output the filtered co-occurrence matrix in both EGAD and Cytoscape format. IN THIS PIPELINE, THE FOLLOWING PYTHON SCRIPT SHOULD BE USED WITH ONLY ONE CORE (-t 1).

python3 -u top1_co_occurrence_matrix_version2_TOP420_removing_ties.py -p $co_ocurrence/co_occurrence_table_def.csv -c $co_ocurrence/agg_filtered_net_Cyto.csv -e $co_ocurrence/agg_filtered_net_EGAD.csv

python3 -u top1_co_occurrence_matrix_version2_TOP420_with_ties.py.py -p $co_ocurrence/co_occurrence_table_def.csv -c $co_ocurrence/agg_full_net_Cyto.csv -e $co_ocurrence/agg_full_net_EGAD.csv

# The "EGAD_final_aggregation.R" will evaluate the final co-occurrence matrix, providing a AUROC value for the given ontology.

Rscript EGAD_final_aggregation.R $scripts/mapman_corrected_stilbenoid_anthocyanins.csv $co_ocurrence/agg_net_EGAD_filtered.csv $co_ocurrence/agg_filtered_egad_out.txt all_experiments

Rscript EGAD_final_aggregation.R $scripts/mapman_corrected_stilbenoid_anthocyanins.csv $co_ocurrence/agg_full_net_EGAD.csv $co_ocurrence/agg_full_net_EGAD.txt all_experiments
