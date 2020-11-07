install.packages("caret")
library(caret)
library(rpart.plot)

lens = read.csv("lenses.data.csv", header = FALSE, col.names = c("1", "2", "3", "4", "5", "Label"))

x = lens[,1:5]
head(x)
#when you want to convert a numeric/integer/character variable into a categorical variable we use as. factor.
y = as.factor(lens$Label)
#Recursive partitioning for classification, regression and survival trees.
model = rpart(y~.,x,control=rpart.control(minsplit=0,minbucket=0,cp=-1, maxcompete=0, maxsurrogate=0, usesurrogate=0, xval=0,maxdepth=5))

plot(model)
text(model)

rpart.plot(model)

#Information Gain
sum(y==predict(model,x,type="class"))/length(y)

#mis classification error
1-sum(y==predict(model,x,type="class"))/length(y)

model1 = rpart(y~.,x,control=rpart.control(minsplit=0,minbucket=0,cp=-1, maxcompete=0, maxsurrogate=0, usesurrogate=0, xval=0,maxdepth=7))

plot(model1)
text(model1)

rpart.plot(model1)

#Information Gain
sum(y==predict(model1,x,type="class"))/length(y)

#mis classification error
1-sum(y==predict(model1,x,type="class"))/length(y)

#Result: If tree depth is increased, the mis classification error has decreased and information gain increased.
