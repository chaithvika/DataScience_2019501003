setwd("C:/Users/kittu/Documents/DS_Specialization/DataScience_2019501003/Data Mining/Data Mining Assignments/DM Assignment2")

data <- read.csv("myfirstdata.csv", header = FALSE)

# Gives us the head of the data
head(data)

#Column Names
names(data)

#description of each column of dataset
str(data)

#dimensions of data Rows by Columns
dim(data)

#plots the data of only first column
plot(data[ , 1])

#plots the data of only second column
plot(data[ , 2])

data1 <- read.csv("myfirstdata.csv", header = FALSE)

head(data1)