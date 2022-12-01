library(DESeq2)
library(edgeR)

#getting args

args = commandArgs(trailingOnly=TRUE)

if (length(args)<5) {
  stop("At least 5 arguments must be supplied -1) path to the folder that contains all counts file, 2) the name of the all counts file, 3) the folder where the PCC matrix will be storaged, 4) path of the file with the gene lenght information and 5) path of the scripts folder."
       , call.=FALSE)
}

##reading the data and generating a DESeqDataSet

path = args[1]
input = args[2]
storage_folder = args[3]
annotations = args[4]
scripts = args[5]
setwd(storage_folder)
temporal = paste(path, '/temporal.txt', sep = '')
filtered = paste(path, '/filtered.txt', sep = '')
print(temporal)
print(filtered)

data = read.table(file = input, header = TRUE, sep ='\t')

final = length(colnames(data))
conteos = (data[7:final])
row.names(conteos) = data$Geneid

columnas = data.frame(colnames(conteos))

diseño <- (matrix(c(1:length(colnames(conteos)))))

dds <- DESeqDataSetFromMatrix(conteos, colData = columnas, design = diseño )

#adding the gene lenght information

load(file = annotations)
rowRanges(dds) <- anno

#computing the FPKM values

values = fpkm(dds)
row.names(values) = rownames(conteos)

write.table(values, file = temporal, sep = '\t', quote = F)

#filtering out genes with less than 0.5 FPKM

#The removal of the genes is done with a homemade python script

setwd(scripts)
system(paste('python3 removing_genes.py -i ', temporal, ' -o ', filtered, sep = ''))

#calculating PCCs

setwd(storage_folder)
system(paste('rm ', temporal, sep = ''))

print(filtered)
data = read.table(file = filtered, header = T, sep = '\t')
data = t(data)

pcc = cor(data, method = "pearson")

output = paste(path, 'PCC.txt', sep = '')
write.table(pcc, file = output, quote = F)
system(paste('rm ', filtered))
