#!/usr/bin/env Rscript
library("optparse")
library("data.table")
library(parallel)
library(igraph)

args = commandArgs(trailingOnly=TRUE)

if (length(args)<2) {
  stop("At least 2 arguments must be supplied: 1)path of the folder with the HRR matrix, 2)path of the output file."
       , call.=FALSE)
}

input_dir = args[1]
#input_dir = '/home/tomslab/Escritorio/Luis/sRA/top_1%/matrices/prueba'
#out = '/home/tomslab/Escritorio/Luis/sRA/top_1%/matrices/prueba/out.csv'
out = args[2]
#cores = integer(args[3])
cores = 21
setwd(input_dir)

files <- list.files()


setDTthreads(threads = cores)
counter = 1

for (file in files){
  print(file)
  name = paste0('value.', counter)
  dt <-  fread(file, sep='\t', header = T, check.names=F, nThread = cores)
    dt <- melt(dt, id.vars = "V1", value.name = name)
    
  if (!exists('final')){
    final <- dt
    colnames(final) <- c("V1", "variable", "value.x")
  }else{
    final <- merge(final, dt, by = c("V1", "variable"), all = T)
    print('merge hecho')
    
  }
    
  if (counter == 25){
    print('New sum')
    vector = c(3:ncol(final))
    
    cl <- makeCluster(21)
    values <- parRapply(cl = cl, x = final[, ..vector], FUN = sum,na.rm=TRUE)
    stopCluster(cl)
    #values = apply(final[, ..vector], 1, sum, na.rm=TRUE)
    final[, grep("value*", colnames(final)):=NULL]
    final[, value.x:=values]
    counter = 0
    
  }  
  counter = counter + 1
}

print('Final sum')
vector = c(3:ncol(final))

cl <- makeCluster(21)
values <- parRapply(cl = cl, x = final[, ..vector], FUN = sum, na.rm=TRUE)
stopCluster(cl)
#final[, sum:=apply(.SD, 1, sum, na.rm=TRUE), by= c("V1", "variable") ]
#final[, value.x := sum(colnames(final)[3:length(colnames(final))],na.rm = T), by = c("V1", "variable")]

final[, grep("value*", colnames(final)):=NULL]
final[, sum:=values]
#g <- graph.data.frame(final, directed=FALSE)
#final = get.adjacency(g, attr="sum", sparse=FALSE)
final2 = dcast(final, formula = V1~factor(variable, levels = unique(V1)), value.var = 'sum', fill = 0)

fwrite(final2, file = out, quote = F, row.names = F, col.names = T, nThread = cores, sep = '\t')
