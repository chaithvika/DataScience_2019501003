setwd("C:/Users/kittu/Documents/DS_Specialization/DataScience_2019501003/Data Mining/Data Mining Assignments/DM Assignment2")

data <- read.csv("twomillion.csv", header = FALSE)

head(data)

str(data)

dim(data)

library(dplyr)

#Sampling 10000 lines
myData_sample_10000 <- sample_n(data, 10000) 

dim(myData_sample_10000)

max(myData_sample_10000)

min(myData_sample_10000)

var(myData_sample_10000)

mean(myData_sample_10000)

quantile(myData_sample_10000$V1,  probs = c(0.25))

summary(myData_sample_10000)

summary(data)

write.csv(myData_sample_10000, file = "C:/Users/kittu/Documents/DS_Specialization/DataScience_2019501003/Data Mining/Data Mining Assignments/DM Assignment2/Sample_data.csv")