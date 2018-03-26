library("ggplot2")
library("dplyr")

input <- "tcost-PW.csv"

pdf("progress-increasing-PW.pdf", width = 3.3, height = 1)

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

ggplot(summary, aes(x = size, y = mean, shape = mode)) +
  geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), color = "black", size=0.5, width=0.25) +
  geom_line(size = 0.4, aes(linetype = mode)) +
  geom_point(size = 3) +
  scale_x_discrete(limits = 1:5) +
  theme_bw() + 
  theme(
    text=element_text(size=9),
    axis.title.x = element_text(size=10.2),
    legend.position = "none",
    plot.margin=unit(c(0.1,0.02,0.1,0.05), "cm"), #(top,right,bottom,left)
    axis.title.y = element_text(margin = margin(t = 0, r = 2, b = 0, l = 0), size=10),
    axis.text.y = element_text(margin = margin(t = 0, r = 0.8, b = 0, l = 1)),
    panel.border = element_rect(size=0.6)
  ) +
  labs(x = "Number of conflicts", y = "Time (m)")
