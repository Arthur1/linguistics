library(maptools)


par(family='sans')
data <- read.csv('./pickup/result.csv', header=F, sep=',')
plot(data$V2, data$V3, xlab='karaoke', ylab='usen')
pointLabel(x=data$V2, y=data$V3, labels=data$V1)
lm.obj <- lm(data$V3 ~ data$V2)
abline(lm.obj, col=2)
