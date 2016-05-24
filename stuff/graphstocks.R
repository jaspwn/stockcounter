#!/usr/bin/env Rscript
library(lubridate)
library(ggplot2)

args <- commandArgs(trailingOnly = TRUE)

#data <- read.csv('/home/jason/Dropbox/Python/stockusage.txt', stringsAsFactors = FALSE)
data <- read.csv(args[1], stringsAsFactors = FALSE)

## Find start and end date of data for plot title
dates <- data$date
POSIXtime <- as.POSIXct(strptime(dates, format='%d-%m-%Y'))
startdate <- min(POSIXtime)
enddate <- max(POSIXtime)


## Count the number of times each stock was used
counts <- as.data.frame(table(data$stock))

## Plot stock usage

plot <- ggplot(data = counts, aes(x = Var1, y = Freq)) +
  geom_bar(stat = 'identity') +
  ylab('Number of times used') +
  xlab('Stock number') +
  ggtitle(paste('Stock usage from', startdate, 'to', enddate)) +
  theme_grey(base_size = 18)

## Output plot
ggsave(filename = paste('Stock usage from', startdate, 'to', enddate, '.pdf'), plot = last_plot())

