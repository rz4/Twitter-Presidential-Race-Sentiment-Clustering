#Twitter_Presedential_Race_Sentiment_Clustering: GraphTwitterData.R
#Authors: Rafael Zamora and Justin Murphey
#Last Updated: 12/4/16

#This R script is used to graph and export processed and clustered twitter data.

#Setup Parameters
library(e1071)
library(ggplot2)
path_to_data = "/Twitter_Presidential_Race_Sentiment_Clustering/data/"
path_to_results = "/Twitter_Presidential_Race_Sentiment_Clustering/results/"
path_to_figures = "/Twitter_Presidential_Race_Sentiment_Clustering/doc/figures/"

#Export PNGS of processed data graphs
files <- list.files(path=paste(path_to_data,"processed/",sep=""), pattern="*.csv", full.names=T, recursive=FALSE)
lapply(files, function(x){
  png_filename = paste(substr(basename(x), 1, nchar(basename(x)) - 4) , ".png",sep="")
  data = read.csv(file=x, head=FALSE, sep=",")
  colnames(data)[1] = 'Sentiment'
  colnames(data)[2] = 'Candidate_Value'
  centroid = data.frame(c(mean(data_[[1]])),c(mean(data_[[2]])))
  colnames(centroid)[1] = 'Sentiment'
  colnames(centroid)[2] = 'Candidate_Value'
  p = ggplot(data_, aes(x=Candidate_Value, y=Sentiment)) + geom_point(size=I(.3))
  p = p + labs(title=basename(x), x ="Candidate_Value", y = "Sentiment") + coord_cartesian(xlim = c(-1,1),ylim = c(-1,1))
  p = p + geom_point(data=centroid, aes(color="Centroid"), size=5) + theme(legend.position="none")
  ggsave(filename=paste(path_to_figures, png_filename,sep=""), plot=p, width=11, height=8.5, units='in')
})

#Export PNGS of clustered data grpahs
files <- list.files(path=path_to_results, pattern="*.csv", full.names=T, recursive=FALSE)
lapply(files, function(x){
  png_filename = paste(substr(basename(x), 1, nchar(basename(x)) - 4) , ".png",sep="")
  data = read.csv(file=x, head=FALSE, sep=",")
  colnames(data)[1] = 'Sentiment'
  colnames(data)[2] = 'Candidate_Value'
  colnames(data)[3] = 'Cluster'
  data$Cluster = as.character(data$Cluster)
  p = ggplot(data, aes(x=Candidate_Value, y=Sentiment, color=Cluster, shape=Cluster)) + geom_point(size=I(.75)) + scale_fill_hue(l=40) + scale_shape_manual(values=1:20)
  p = p + labs(title=basename(x), x ="Candidate_Value", y = "Sentiment") + coord_cartesian(xlim = c(-1,1),ylim = c(-1,1))
  ggsave(filename=paste(path_to_figures, png_filename,sep=""), plot=p, width=11, height=8.5, units='in')
})
