library(EGAD)

#taking arguments

args = commandArgs(trailingOnly=TRUE)

if (length(args)<4) {
  stop("At least 4 arguments must be supplied: 1)path of the ontology file, 2)path of the network file, 3)path of the AUROCs values file. and 4)number of the iteration where the AUROC values loop is at"
       , call.=FALSE)
}

anno_file = args[1]
network_file = args[2]
output = args[3]
iteration = args[4]

#loading the annotations matrix

print('Loading ontology')

anno = read.table(file = anno_file, sep = '\t', header = T)

names = colnames(anno)
true_names = c()

for (name in names){
  name = strsplit(name, 'X')[[1]][2]
  true_names = c(true_names, name)
}

colnames(anno) = true_names

#loading the gene network

print('Loading gene network')

gene_network = read.table(file = network_file, sep = '\t', header = T)

row.names(gene_network) = gene_network$X
gene_network$X = NULL

#running neighbor voting algorithm

print('Running neighbor voting algorithm')

vector = 1:10

for (number in vector){
  
  GO_groups_voted <- run_GBA(as.matrix(gene_network), as.matrix(anno))
  auroc = GO_groups_voted[[3]]
  
  out = file(output, 'a')
  sentence = paste0(auroc, '\t', iteration, '\tAggregated')
  print('Ignore the following writing warning')
  write(sentence, file = out, append = T)
}


#GO_multifunc_assessment <- calculate_multifunc(anno)
#auc_mf <- auc_multifunc(anno, GO_multifunc_assessment$MF.rank)
