library("ggplot2")
library("dplyr")
library("grid")
library("gridExtra")

# df<-read.csv("wp-capacity-all-FINAL.csv")
# pdf("get-time.pdf", width=3.7, height=3)
# ggplot(df, aes(x=n, y=get_time)) + geom_point(size=0.3)

# pdf("activation-time1.pdf", width=3.8, height=2)
# ggplot(df, aes(x=n, y=activation_time, shape=mode, colour=mode)) +
#    geom_vline(xintercept=168, linetype="dotted", color = "red") +
#    geom_vline(xintercept=939, linetype="dotted", color = "blue") +
#    theme_bw() +
#    theme(
#      legend.position = c(.98, .95),
#      legend.title = element_blank(),
#      legend.justification = c("right", "top"),
#      legend.box.just = "right",
#      legend.margin = margin(0, 0, 0, 0)
#    ) +
#    guides(colour = guide_legend(override.aes = list(size = 3))) +
#    geom_point() +
#    labs(y="Activation time\n(in seconds)", x="Plugin id")

df<-read.csv("capacity-default.csv")

pdf("teste.pdf", width=3.8, height=2)
# width = 2.5, height = 2

first <- ggplot(df, aes(x=n, y=activation_time, group=mode)) +
   geom_vline(xintercept=168, linetype="dotted", color = "black") +
   geom_point(size = 1) +
   theme_bw() +
   theme(
     plot.title = element_text(size=8, hjust = 0.5, vjust= -1.5),
     text=element_text(size=8),
     legend.position = "none",
     axis.title.x=element_blank(),
     axis.text.x=element_blank(),
     axis.ticks.x=element_blank(),
     axis.line=element_blank(),
    #  plot.margin=unit(c(0.2,0.21,0.2,0.21), "cm"), # (top,right,bottom,left)
     plot.margin=unit(c(-1,1,5,1), "mm"), # (top,right,bottom,left)
   ) +
   guides(colour = guide_legend(override.aes = list(size = 1))) +
   scale_shape_manual(labels = c('default')) +
   labs(title="Running configuration with default settings", y="Activate time\n(in seconds)", x="Plugin id") +
  #  scale_x_continuous(breaks = round(seq(0, 1300, by = 200),1)) +
   scale_x_continuous(labels = function (x) floor(x), limits = c(0,1300), breaks = round(seq(0, 1300, by = 200),1)) +
   scale_y_continuous(labels = function (x) floor(x), limits = c(0,20))

df2<-read.csv("capacity-modified.csv")

second <- ggplot(df2, aes(x=n, y=activation_time, group=mode)) +
   geom_vline(xintercept=939, linetype="dotted", color = "black") +
   geom_point(size = 1) +
   theme_bw() +
   theme(
     plot.title = element_text(size=8, hjust = 0.5, vjust= -1.5),
     legend.title = element_blank(),
     text=element_text(size=8),
     legend.position = "none",
    #  plot.margin=unit(c(-0.2,0.2,0,0.2), "cm"), # (top,right,bottom,left)
    #  legend.margin = margin(0, 0, 0, 0),
    #  plot.margin=unit(c(0,0,0,0), "cm")
   ) +
   guides(colour = guide_legend(override.aes = list(size = 1))) +
   scale_shape_manual(labels = c('modified')) +
   labs(title="Running configuration with tweaks", y="Activate time\n(in seconds)", x="Plugin id") +   
   scale_x_continuous(breaks = round(seq(0, 1300, by = 200),1))+
   scale_y_continuous(labels = function (x) floor(x), limits = c(0,20))

grid.arrange(first, second, ncol=1)

#####################

# df<-read.csv("wp-capacity-all-FINAL.csv")
# pdf("activation-time1.pdf", width=3.8, height=2)
# ggplot(df, aes(x=n, y=activation_time, group=mode, shape=mode, colour=mode)) +
#    geom_vline(xintercept=168, linetype="dotted", color = "red") +
#    geom_vline(xintercept=939, linetype="dotted", color = "blue") +
#    geom_point(size = 1) +
#    theme_bw() +
#    theme(
#      legend.position = c(.98, .95),
#      legend.title = element_blank(),
#      legend.justification = c("right", "top"),
#      legend.box.just = "right",
#      legend.margin = margin(0, 0, 0, 0)
#    ) +
#    guides(colour = guide_legend(override.aes = list(size = 1))) +
#   #  scale_color_manual(values = c('red', 'blue'), labels = c('default', 'modified')) +
#    scale_shape_manual(values = c(21, 24), labels = c('default', 'modified')) +
#    labs(y="Activation time\n(in seconds)", x="Plugin id") 
#   #  scale_x_continuous(breaks = round(seq(1, 1000, by = 100),1))
