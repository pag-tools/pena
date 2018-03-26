library("ggplot2")
library("dplyr")

input <- "tcost.csv"

pdf("iterative-increasing.pdf", width = 3, height = 1.3)
# par(pin=c(4,0.7*4))

df <- read.csv(input, header = F)
colnames(df) <- c("secs", "size", "mode", "iter")
df <- mutate(df, time = secs / 60)

summary <- summarise(group_by(df, mode, size),
                     n = length(iter),
                     mean = mean(iter),
                     sd = sd(iter),
                     se = sd / sqrt(n))

# DEBUG
summary

ggplot(summary, aes(x = size, y = mean)) +
  geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), size=0.5, width=0.25) +
  geom_line(size = 0.3) +
  geom_point(size = 2) +
  scale_x_discrete(limits = 1:5) +
  theme_bw() + 
  theme(text=element_text(size=8),
        legend.background = element_blank(),
        legend.title = element_blank()) +
  labs(x = "Number of conflicts", y = "Number of reruns")

