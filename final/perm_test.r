lcg <- read.csv("lcg.csv", header=T)
bbs <- read.csv("bbs.csv", header=T)

#Examine data, looking at summary
length(lcg$runtime)
mean(lcg$runtime)
var(lcg$runtime)
sd(lcg$runtime)
quantile(lcg$runtime)
hist(lcg$runtime)

length(bbs$runtime)
mean(bbs$runtime)
var(bbs$runtime)
sd(bbs$runtime)
quantile(bbs$runtime)
hist(bbs$runtime)

# Cannot assume Normality based on sample distribution, therefore use Perm Test
perm.test <- function(v1, v2, num_splits=10000){
    n1 <- length(v1)
    n2 <- length(v2)

    xbar1 <- mean(v1)
    xbar2 <- mean(v2)
    stat_of_interest <- xbar1 - xbar2

    combined_vectors <- c(v1, v2)
    xbar_difs <- NULL

    for(i in 1:num_splits){
        mix <- sample(combined_vectors)
        new_v1 <- mix[1:n1]
        new_v2 <- mix[(n1+1):(n1+n2)]

        xbar_dif <- mean(new_v1) - mean(new_v2)
        xbar_difs <- c(xbar_difs, xbar_dif)
    }

    hist(xbar_difs)
    abline(v=stat_of_interest,lty=2)

    pval <- length(xbar_difs[xbar_difs > stat_of_interest])
    pval <- (pval + 1) / (length(xbar_difs) + 1) # +1 due to pg 43
    pval <- 2 * pval

    return(list(pval, xbar_difs, stat_of_interest))
}

# Two-Tailed Test
perm_results <- perm.test(bbs$runtime, lcg$runtime)

pval <- perm_results[1]
xbar_difs <- unlist(perm_results[2])
original_xbar_dif <- perm_results[3]

length(xbar_difs)
mean(xbar_difs)
var(xbar_difs)
sd(xbar_difs)
quantile(xbar_difs)
