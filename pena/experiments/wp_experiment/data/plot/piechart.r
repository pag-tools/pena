# library(ggplot2)
# library(dplyr)

# steps <- c("Delta of initial fetching", "Delta of searching", "Delta of cleansing", "Delta of visual oracle")
# hours <- c(77.4, 464.65, 73.8, 2.3) # in minutes

# subjects_table <- data.frame(steps, hours) 
# colnames(subjects_table) <- c("Deltas", "Total")
# subjects_total <- sum(subjects_table[,2])
# subjects_total

# # ggplot(subjects_table, aes(x="",y=Total, fill= Deltas)) +
# # geom_bar(width = 1,color="white", stat="identity") +
# # coord_polar(theta="y", start=0) +
# # labs(y="", x="") +
# # guides(fill = guide_legend(reverse = TRUE))

# # Why Barplot Is Not A Good Visual:

# ggplot(subjects_table, aes(x = "", y = Total, fill = Deltas)) +
# geom_bar(width = 1, color="white", stat = "identity")

library("ggplot2")
library("dplyr")
# expression(delta)
# deltas <- c("1. Delta to fetching pages", "2. Delta", "3. Conflicts cleansing", "4. Visual oracle")
# time <- c(81.66, 195.98, 71.8, 2.73) # in minutes
deltas <- c("1. Delta to fetching pages", "2. Conflicts cleansing", "3. Visual oracle", "4. Others")
time <- c(298.51, 145.63, 2.6, 0.37 ) # in minutes

subjects_table <- data.frame(deltas, time)
colnames(subjects_table) <- c("Iterations", "Time (in minutes)")

pdf("delta-consuming.pdf", width = 3.5, height = 1.3)

subjects_table

my.labs <- list(bquote(delta), "2. Conflicts cleansing", "3. Visual oracle", "4. Others")

ggplot(subjects_table, aes(x = deltas, y = time, fill=deltas)) + 
geom_bar(stat = "identity") +
scale_fill_brewer(palette="OrRd") +
theme_bw()+
theme(text=element_text(size=8),
    legend.background = element_blank(),
    legend.title = element_blank(),
    # axis.title.y = element_text(size=8),
    # axis.text.y = element_text(size=8),
) +
scale_y_continuous( limits = c(0,300) ) +
scale_x_discrete(labels = c(1,2,3,4)) +
scale_colour_manual(values=1:2,breaks=deltas,
                      labels=my.labs) +
labs(x="Steps", y = "Time (in minutes)")