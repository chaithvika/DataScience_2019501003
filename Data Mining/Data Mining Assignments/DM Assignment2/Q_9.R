setwd("C:/Users/kittu/Documents/DS_Specialization/DataScience_2019501003/Data Mining/Data Mining Assignments/DM Assignment2")

data <- read.csv("OH_house_prices.csv", header = FALSE)

head(data)

names(data)

median(data$V1)

mean(data$V1)