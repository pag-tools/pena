library("ggplot2")
library("dplyr")
library("grid")
library("gridExtra")

ssinput <- "tcost-SS.csv"
itinput <- "it-tcost.csv"
pwinput <- "tcost-PW.csv"

pdf("progress-increasing-merge.pdf", width = 2.5, height = 2)

df <- read.csv(ssinput, header = F)
itdf <- read.csv(itinput, header = F)
pwdf <- read.csv(pwinput, header = F)

colnames(df) <- c("secs", "size", "mode")
colnames(itdf) <- c("secs", "size", "mode", "iter")
colnames(pwdf) <- c("secs", "size", "mode")

df <- mutate(df, time = secs / 60)
itdf <- mutate(itdf, time = secs / 60)
pwdf <- mutate(pwdf, time = secs / 60)

summary <- summarise(group_by(df, mode, size),
                     n = length(time),
                     mean = mean(time),
                     sd = sd(time),
                     se = sd / sqrt(n))

itsummary <- summarise(group_by(itdf, mode, size),
                     n = length(iter),
                     mean = mean(iter),
                     sd = sd(iter),
                     se = sd / sqrt(n))

pwsummary <- summarise(group_by(pwdf, mode, size),
                     n = length(time),
                     mean = mean(time),
                     sd = sd(time),
                     se = sd / sqrt(n))

summary
itsummary
pwsummary

pwplot <- ggplot(pwsummary, aes(x = size, y = mean, shape = mode)) +
# geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), color = "black", size=0.5, width=0.25) +
  geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), color = "black", size=0.2, width=0.1) +
  geom_line(size = 0.3, aes(linetype = mode)) +
  geom_point(size = 1.2) +
  scale_x_discrete(limits = 1:5) +
  theme_bw() + 
  theme(
    text=element_text(size=8),
    legend.position = "none",
    # plot.margin=unit(c(0.1,0,0.5,-0.1), "cm"), #(top,right,bottom,left)
    plot.margin=unit(c(0.1,0,0.5,0.35), "cm"),
    # axis.title.y = element_text(margin = margin(t = 0, r = 1, b = 0, l = 4), size=8),
    axis.text.y = element_text(margin = margin(t = 0, r = 1, b = 0, l = 2), size=6),
    axis.title.y=element_blank(),
    axis.title.x=element_blank(),
    axis.text.x=element_blank(),
    axis.ticks.x=element_blank(),
    axis.line=element_blank(),
  ) +
  annotate("label", x = 5.5, y = 232, label = "PW", size=2, fontface="bold") +
  labs(y = "Time (m)")

itplot <- ggplot(summary, aes(x = size, y = mean)) +
# geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), color = "black", size=0.5, width=0.25) +
  geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), color = "black", size=0.2, width=0.1) +
  geom_line(size = 0.3, aes(linetype = mode)) +
  geom_point(size = 1) +
  scale_x_discrete(limits = 1:5) +
  theme_bw() + 
  scale_y_continuous(labels = function (x) floor(x), limits = c(4,16)) +
  theme(
    text=element_text(size=8),
    legend.position = "none",
    axis.title.x=element_blank(),
    axis.text.x=element_blank(),
    axis.ticks.x=element_blank(),
    axis.line=element_blank(),
    # plot.margin=unit(c(-0.5,0,1,-0.10), "cm"),#(top,right,bottom,left)
    plot.margin=unit(c(-0.5,0,1,-0.10), "cm"),#(top,right,bottom,left)
    axis.title.y = element_text(margin = margin(t = 0, r = 3, b = 0, l = 4), size=8),
    axis.text.y = element_text(margin = margin(t = 0, r = 1, b = 0, l = 3), size=6),
    ) +
  annotate("label", x = 5.5, y = 15, label = "SS", size=2, fontface="bold") +
  labs(y = "                 Time (in minutes)")

rerun <- ggplot(itsummary, aes(x = size, y = mean)) +
# geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), color = "black", size=0.5, width=0.25) +
  geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), color = "black", size=0.2, width=0.1) +
  geom_line(size = 0.3) +
  geom_point(size = 1) +
  scale_x_discrete(limits = 1:5) +
  theme_bw() + 
  scale_y_continuous( limits = c(-1,6) ) +
  theme(text=element_text(size=8),
        legend.background = element_blank(),
        legend.title = element_blank(),
        plot.margin=unit(c(-1,0,0,-0.10), "cm"),#(top,right,bottom,left)
        axis.title.y = element_text(margin = margin(t = 0, r = 8.5, b = 0, l = 4), size=8),
        axis.text.y = element_text(margin = margin(t = 0, r = 1, b = 0, l = 3), size=6),
  ) +
  annotate("label", x = 5.5, y = 5.5, label = "SS", size=2, fontface="bold") +
  labs(x = "Number of conflicts", y = "# Iterations")

# grid.arrange(pwplot, itplot, rerun, ncol=1, heights = c(1, 1, 1))
grid.arrange(pwplot, itplot, rerun, ncol=1, heights = c(0.8,0.8,0.5))
