library("ggplot2")
library("dplyr")

input <- "tcost.csv"

pdf("progress-increasing.pdf", width = 3.0, height = 1.3)

df <- read.csv(input, header = F)
colnames(df) <- c("secs", "size", "mode")
df <- mutate(df, time = secs / 60)

summary <- summarise(group_by(df, mode, size),
                     n = length(time),
                     mean = mean(time),
                     sd = sd(time),
                     se = sd / sqrt(n))

# DEBUG
summary

ggplot(summary, aes(x = size, y = mean, colour = mode, shape = mode)) +
  geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), color = "black", size=0.5, width=0.25) +
  geom_line(size = 0.3, aes(linetype = mode)) +
  geom_point(size = 1.5) +
  annotate("text", x = 0.5, y = 200, label = "PW", size=3) +
  annotate("text", x = 0.5, y = 25, label = "SS", size=3) +
  scale_x_discrete(limits = 1:5) +
  theme_bw() + 
  theme(text=element_text(size=8),
          legend.position = "none") +
  labs(x = "Number of conflicts", y = "Time")
