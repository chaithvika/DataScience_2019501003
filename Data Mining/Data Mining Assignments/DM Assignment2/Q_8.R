setwd("C:/Users/kittu/Documents/DS_Specialization/DataScience_2019501003/Data Mining/Data Mining Assignments/DM Assignment2")

data <- read.csv("football.csv", header = TRUE)

names(data)

head(data)

str(data)

plot(X2004.Wins ~ X2003.Wins, data = data, main = "Scatter Plot : 2003 Wins vs 2004 Wins")

cor(data$X2003.Wins, data$X2004.Wins)

data1 <- data

data1 <- data1[,3] * 2

head(data1)

cor(data$X2003.Wins, data1)