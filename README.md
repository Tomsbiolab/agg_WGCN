# agg_WGCN
Pipeline for generating full and filtered GCNs

IMPORTANT: This pipeline is suposed to work after the execution of the networks_alignment pipeline, available at (). This readme file helps the user to execute the pipeline. Information about how the pipeline works is available at CITE PAPER.

This pipeline is controlled by the "slurm_aggregated_network.sh" master script. The script is designed for working with SLURM. The master script has parameters that should be edited by the user. These parameters are:

1- metadata_file: Path to the file that contains the information of all the aligned runs. The most important column of the metadata file is the first one, that should contain the tissue from which each run is coming from. Example of this file is available at "metadata_example.csv".

2- count_summaries_folder: Path to the folder that contains the count summaries generated by the networks_alignment pipeline. 

3- count_matrices_folder: Path to the folder that contains the raw count matrices generated by the networks_alignment pipeline.

4- tissue: Tissue selected for constructing the network. It has to be a tissue present in the first column of the metadata_file. As indicated in the master script, if you want to do a network of more than one tissue, you have to list the tissues separated by a semicolon(e.j. leaf;berry will do the network of both leaf and berry tissues combined). If you want to do a condition independent network, tissue has to be 'ALL'. 

5- result_folder: Path to the folder where the network is going to be constructed. The pipeline will automatically generate the needed subfolders inside the base folder. 

6- scripts: Path to the folder where the scripts of this pipeline are storaged.

7- anno: Path to the .rda file that contains the annotations of the genome in GRanges format. Example of this file is available at "annotations.rda"

If you have any question, please contact us at luis.orduna(at)uv.es