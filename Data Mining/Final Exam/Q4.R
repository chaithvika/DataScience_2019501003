liver = read.csv("Liver_data.csv", header = FALSE, col.names = c("mcv", "alkphos", "sgpt", "sgot", "gammagt", "drinks","selector"))

liver$selector <- as.factor(liver$selector)
#The cut function is often quite useful for making discrete variables from continuous or numerical ones, sometimes in combination with the function quantile.
#we can group some of the data together.
liver$drinks <- cut(liver$drinks, breaks = c(0,5,10,15,20), labels = c('C1', 'C2', "C3", 'C4'), right = FALSE)
#for omiting null variable
liver <- na.omit(liver)

#subset is for taking a small subset of the given data upon a condition
#contains all the 7 columns
train = subset(liver, liver$selector == 1)
test = subset(liver, liver$selector == 2)

#contains 5 columns. Removed selector and drinks. 
#Selector is used for spliting test and train data. drinks is the categorical output which we have to find
x_train <- subset(train, select = -c(selector, drinks))
x_test <- subset(test, select = -c(selector, drinks))

library(class)
#contains only drinks
y_train = train[,6, drop = TRUE]
y_test = test[,6, drop = TRUE]

#k = 1
fit1 = knn(x_train,x_train,y_train,k=1)  
1-sum(y_train==fit1)/length(y_train) 
#Misclassification error: 0
1-sum(y_test==fit1)/length(y_test)   
# Misclassification error : 0.515

#K = 2
fit2 = knn(x_train,x_train,y_train,k=2)
1-sum(y_train==fit2)/length(y_train)
#Misclassification error: 0.1468531
1-sum(y_test==fit2)/length(y_test)
#Misclassification error: 0.46

#k = 3
fit3 = knn(x_train,x_train,y_train,k=3)
1-sum(y_train==fit3)/length(y_train)
#Misclassification error: 0.1818182
1-sum(y_test==fit3)/length(y_test)
#Misclassification error: 0.47