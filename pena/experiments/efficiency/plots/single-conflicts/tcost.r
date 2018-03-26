library("ggplot2")
library("dplyr")

input <- "tcost.csv"
pdf("progress.pdf", width = 3.0, height = 1.3)

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

pd <- position_dodge(0.1) # to not overlap x points
ggplot(summary, aes(x = size, y = mean, colour = mode, shape = mode)) +
  geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd),
                width = 2, # 3
                position = pd,
                color = "black",
                 size=2) + # size=0
  geom_line(position = pd, size = 0.3, aes(linetype = mode)) +
  geom_point(position = pd, size = 1) +
  theme_bw() +
  scale_x_continuous(limits=c(0, 160)) +
  theme(text=element_text(size=8),
        legend.position = c(.09, .7),
        legend.background = element_blank(),
        legend.title= element_blank())  +
  labs(x="Number of Plugins", y="Time (in minutes)")