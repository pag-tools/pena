library("ggplot2")
library("dplyr")

input <- "histogram.csv"
input <- read.table("histogram.txt", header=TRUE)
pdf("recall_histogram.pdf", width = 3.0, height = 1.3)

################# by txt
# qplot(input$CONFLICTS, geom="histogram")
ggplot(data=input, aes(input$CONFLICTS)) + geom_histogram(bins=5, col="white") +
labs(x="Conflicts", y="Frequency")+
theme(
    axis.text=element_text(size=10),
    axis.title=element_text(size=14),
    axis.title.y = element_text(margin = margin(t=0, r = 5, b = 0, l = 0))
)
# axis.text=element_text(size=12),
# axis.title=element_text(size=14,face="bold")

# ggplot(data=input, aes(input$RUNS)) + geom_bar() +
# labs(x="Runs", y="Conflicts") +
# scale_x_discrete(limits=c("1","2","3","4","5","6","7","8","9","10")) +
# ylim(c(0,5)) +
#################

# df <- read.csv(input, header = F)
# colnames(df) <- c("runs", "conflicts")
# df <- mutate(df)
# summary <- summarise(group_by(df, runs, conflicts))
# summary
# ggplot(summary, aes(x = runs, y = conflicts)) +
# geom_histogram() 
# labs(x="Runs", y="Conflicts") + 
# xlim(c(1,10)) +
# ylim(c(0,5)) +
# scale_x_continuous(breaks=seq(1,10))
