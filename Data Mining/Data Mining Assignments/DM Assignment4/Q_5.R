setwd("C:/Users/kittu/Downloads/DM Assignments/DM Assignment4")

data <- read.csv("sonar_test.csv", header = FALSE)

head(data)

library(caret)
library(rpart.plot)

x = data[ , 1 : 60]
y = as.factor(data$V61)

model = rpart(y~., x , control = rpart.control(minsplit = 0,minbucket = 0,cp = -1, maxcompete = 0, maxsurrogate = 0, usesurrogate = 0, xval = 0, maxdepth = 5))

plot(model)
text(model)

rpart.plot(model)

# misclassification error
1 - sum(y == predict(model, x, type = "class"))/ length(y)