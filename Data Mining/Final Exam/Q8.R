sensexdata = read.csv("BSE_Sensex_Index.csv", header = TRUE)

#In R programming, the mutate function is used to create a new variable from a data set. 
#In order to use the function, we need to install the dplyr package, which is an add-on to R that 
#includes a host of cool functions for selecting, filtering, grouping, and arranging data.
#getting growth_rate column
library(dplyr)
new_sensexdata = mutate(sensexdata, growth_rate = lead((lag(Close) - Close) / Close))

#last row in growth_rate column
lastcol = nrow(new_sensexdata)
new_sensexdata$growth_rate[lastcol] = mean(new_sensexdata$growth_rate[c((lastcol-3) : (lastcol-1))])

#calculating z-scores
growth_rate_mean <- mean(new_sensexdata$growth_rate, na.rm=TRUE)
growth_rate_sd <- sd(new_sensexdata$growth_rate,na.rm=TRUE)
z<-(new_sensexdata[,8] - growth_rate_mean) / growth_rate_sd
sort(z)
new_sensexdata$zscores <- z

#Dates of the outliers 
dates <- subset(new_sensexdata[,1],  new_sensexdata[,"zscores"] >= 3.0 | new_sensexdata[,"zscores"] <= -3.0)
View(dates)