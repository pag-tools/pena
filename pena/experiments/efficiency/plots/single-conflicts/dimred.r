library(ggplot2)
library("dplyr")

input <- "dimred.csv"
pdf("dimred.pdf", width = 3.0, height = 1.3)
# par(pin=c(4,0.7*4))

df <- read.csv(input, header = T)

summary <- summarise(group_by(df, n), total = length(red), mean = mean(red), sd = sd(red))

# DEBUG
summary

ggplot(summary, aes(x = n, y = mean)) +
  geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), width = 3) +
  geom_line() +
  geom_point() +
  theme_bw() +
  theme(text=element_text(size=8)) +
  labs(x="Before Reduction", y="After Reduction")
