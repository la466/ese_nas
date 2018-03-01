library("ggplot2")
setwd("~/Documents/scripts/ese_nas/")

ESE_sets <- c("ESR", "Ke400_ESEs", "PESE", "RESCUE", "INT3", "RBP_motifs")

for (set in ESE_sets) {
  file_path <- paste("output_data/", set, "_stop_counts.csv", sep="")
  file <- read.csv(file_path, sep=",", head=T)
  simulants <- file[file$id != 'real',]
  real <- file[file$id == 'real',]
  
  print(nrow(simulants))

  plot <- ggplot(data=simulants, aes(simulants$stop_count)) + 
    geom_histogram(breaks=seq(min(file$stop_count), max(file$stop_count), by = 2), col="black", fill="white", alpha = .8) + 
    labs(title=paste(sprintf(set), " (", nrow(simulants), " simulations)", sep="")) +
    labs(x="Stop codon count in all frames", y="Count") + 
    geom_vline(xintercept=file$stop_count[file$id == "real"], lty=2)

  out_path = paste("output_data/", set, "_hist.pdf", sep="")
  ggsave(out_path, plot=plot)
}




