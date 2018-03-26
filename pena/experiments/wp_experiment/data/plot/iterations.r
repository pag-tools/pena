library("ggplot2")
library("ggrepel")
library("dplyr")

iterations <- c("1", "2", "3", "4", "5", "6", "7", "8", "9")
time <- c(214.81,42.48,21.16,10.7,5.13,2.35,1.11,0.66,0.1) # in minutes
conflicts <- c(236, 128, 64, 32, 16, 8, 4, 2, 1)

ttt <- c("Conflicts")

subjects_table <- data.frame(iterations, time)
colnames(subjects_table) <- c("Iterations", "Time (in minutes)")

pdf("time-conflicts-iterations.pdf", width = 3, height = 1.2)

subjects_table

ggplot(subjects_table, aes(x = iterations, y = time, group=1)) + 
geom_line() +
geom_point() +
geom_text(aes(label=conflicts),hjust=0, vjust=-1, size=2) +
theme_bw()+
guides(colour = guide_legend(nrow = 1))+
theme(text=element_text(size=8),
    legend.background = element_blank(),
    legend.title = element_blank(),
    # axis.title.y = element_text(size=8),
    # axis.text.y = element_text(size=8),
) +
# geom_label_repel(
#         aes(iterations, time, label = ttt),
#         box.padding = 0.1, point.padding = 0.1,
#         segment.color = 'grey50') +
annotate("text",x=2.2,y=253,label="conflicts",size=2)+
theme() +
# geom_segment(aes(x = 5, y = 200, xend = iterations, yend = time), 
#     colour='black', size=0.1,arrow = arrow(length = unit(0.1, "cm")))+
scale_y_continuous( limits = c(0,300) ) +
labs(x="Number of Iterations", y = "Time (in minutes)")
# geom_label_repel(
#         aes(iterations, time, label = iterations),
#         box.padding = 0.35, point.padding = 0.5,
#         segment.color = 'grey50')

# rerun <- ggplot(itsummary, aes(x = size, y = mean)) +
# # geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), color = "black", size=0.5, width=0.25) +
#   geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), color = "black", size=0.2, width=0.1) +
#   geom_line(size = 0.3) +
#   geom_point(size = 1) +
#   scale_x_discrete(limits = 1:5) +
#   theme_bw() + 
#   scale_y_continuous( limits = c(-1,6) ) +
#   theme(text=element_text(size=8),
#         legend.background = element_blank(),
#         legend.title = element_blank(),
#         plot.margin=unit(c(-1,0,0,-0.10), "cm"),#(top,right,bottom,left)
#         axis.title.y = element_text(margin = margin(t = 0, r = 8.5, b = 0, l = 4), size=8),
#         axis.text.y = element_text(margin = margin(t = 0, r = 1, b = 0, l = 3), size=6),
#   ) +
#   annotate("label", x = 5.5, y = 5.5, label = "SS", size=2, fontface="bold") +
#   labs(x = "Number of conflicts", y = "# Iterations")

# # grid.arrange(pwplot, itplot, rerun, ncol=1, heights = c(1, 1, 1))
# # grid.arrange(pwplot, itplot, rerun, ncol=1, heights = c(0.8,0.8,0.5))
