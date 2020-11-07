library(arules)
library(arulesViz)
library(RColorBrewer)

#The read.transactions() function read the file csv file and convert it to a transaction format
#Parameters: Transaction file: name of the csv file
#rm.duplicates : to make sure that we have no duplicate transaction entried
#format : basket (row 1: transaction ids, row 2: list of items)
#sep: separator between items, in this case commas
#cols : column number of transaction IDs
txn = read.transactions(file="ItemList.csv", rm.duplicates= TRUE, format="basket",sep=",",cols=1)

#getting rid of unnecessary quotes in transactions
txn@itemInfo$labels <- gsub("\"","",txn@itemInfo$labels)

#running the apriori algorithm
basket_rules <- apriori(txn, parameter = list(sup = 0.3,target="rules"))

inspect(basket_rules)

#Alternative to inspect() is to convert rules to a dataframe and then use View()
df_basket <- as(basket_rules,"data.frame")
View(df_basket)

plot(basket_rules)
plot(basket_rules, method = "grouped", control = list(k = 5))
plot(basket_rules, method="graph", control=list(type="items"))
plot(basket_rules, method="paracoord",  control=list(alpha=.5, reorder=TRUE))
plot(basket_rules,measure=c("support","lift"),shading="confidence",interactive=T,colour=green)

itemFrequencyPlot(txn, topN = 5, col = rainbow(4))
