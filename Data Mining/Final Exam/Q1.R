# question 1(a)
#Read the given CSV and assigns the data to variable data 
data <- read.csv("BSE_Sensex_Index.csv", header = TRUE)

#prints out the dimensions and the head of the data frame
#dim(data)
#head(data)


data$Date <- as.Date(data$Date,format= "%m/%d/%Y")
diff_Date = c()
for(i in 1:(length(data$Date)-1)){
  diff <- difftime(data[i+1,1], data[i,1], units = "days")
  diff_Date <- append(diff_Date,as.numeric(diff, units = "days")) 
}
diff_Date <- append(diff_Date, 0)

#Gets the successive difference of the rows within a column. And for the last row in the column mean of the above 3 rows is added instead of null
diff_Open <- diff(data$Open)
diff_Open <- append(diff_Open, mean(data[c(-5 : -2), 2]))

diff_High <- diff(data$High)
diff_High <- append(diff_High, mean(data[c(-5 : -2), 3]))

diff_Low <- diff(data$Low)
diff_Low <- append(diff_Low, mean(data[c(-5 : -2), 4]))

diff_Close <- diff(data$Close)
diff_Close <- append(diff_Close, mean(data[c(-5 : -2), 5]))

diff_Volume <- diff(data$Volume)
diff_Volume <- append(diff_Volume, mean(data[c(-5 : -2), 6]))

diff_Adj.Close <- diff(data$Adj.Close)
diff_Adj.Close <- append(diff_Adj.Close, mean(data[c(-5 : -2), 7]))

data <- cbind(data, data.frame(diff_Date, diff_Open, diff_High, diff_Low, diff_Close, diff_Volume, diff_Adj.Close))

#install the dpylr package
library(dplyr)

#Created a sample of 1000 observations with replacement
df1 <- sample_n(data, 1000, replace = TRUE)

#Created a sample of 3000 observations with replacement
df2 <- sample_n(data, 3000, replace = TRUE)

# question 1(b)
summary(df1)
summary(df2)

# question 1(c)
summary(data)

# question 1(d)
boxplot(data$Open, data$Close, data$High, data$Low,
        main = "Multiple boxplots within single graph",
        names = c("open", "close", "high", "low"),
        col = c("orange", "red", "blue", "green"),
        border = "brown"
)

# question 1(e)
hist(data$Close,
     main="Frequency Histogram for Close values",
     xlab="Close Values",
     xlim=c(0,16000),
     breaks = seq(from = 0,to = 16000,by = 2000),
     col="darkmagenta",
     freq=FALSE
)
